CentOS7安装软件个人脚本

### 1、安装python39

```sh
mkdir -p /home/python39 &&
cd /home/python39 &&
yum install -y wget tar zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gcc make libffi-devel&&
wget http://npm.taobao.org/mirrors/python/3.9.0/Python-3.9.0.tgz --no-check-certificate &&
tar -zxvf Python-3.9.0.tgz   &&
cd Python-3.9.0 &&
./configure prefix=/usr/local/python39 &&
make -j8 &&
make install -j8 &&
ln -s /usr/local/python39/bin/python3.9 /usr/bin/python3 &&
ln -s /usr/local/python39/bin/pip3.9 /usr/bin/pip3
```

### 2、安装node_exporter1.4.0

```sh
mkdir -p /etc/node-exporter &&
cd /etc/node-exporter &&
yum install -y wget tar &&
wget https://github.com/prometheus/node_exporter/releases/download/v1.4.0/node_exporter-1.4.0.linux-amd64.tar.gz &&
tar -zxvf node_exporter-1.4.0.linux-amd64.tar.gz &&
cat > /etc/systemd/system/node_exporter.service << EOF &&
[Unit]
Description=node_exporter
After=network.target
[Service]
Type=simple
User=root
ExecStart=/etc/node-exporter/node_exporter-1.4.0.linux-amd64/node_exporter
Restart=always
[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload &&
systemctl start node_exporter &&
systemctl enable node_exporter &&
systemctl start firewalld &&
systemctl enable firewalld &&
firewall-cmd --permanent --add-port=9100/tcp &&
firewall-cmd --reload &&
systemctl stop firewalld &&
systemctl disable firewalld
```

### 2.1、或者使用py文件，基于python3开发，需要把node_exporter-1.4.0.linux-amd64.tar.gz放在当前目录，[下载地址](https://github.com/prometheus/node_exporter/releases/download/v1.4.0/node_exporter-1.4.0.linux-amd64.tar.gz)

先安装第三方模块`python -m pip install paramiko`

理论上可以下载其他版本的node exporter放在当前目录即可

```python
import os

import paramiko
from paramiko.client import SSHClient


def traverse_folder(folder, only_first=False):
    folder = os.path.abspath(folder)
    all_files = []
    all_dirs = []
    if os.path.isdir(folder):
        for root, dirs, files in os.walk(folder):
            for one_file in files:
                all_files.append(os.path.join(root, one_file))  # 所有文件
            for one_dir in dirs:
                all_dirs.append(os.path.join(root, one_dir))  # 所有文件夹
            if only_first:
                break
    else:
        msg = 'Can not find folder:{} for traverse'.format(folder)
        print(msg)
    return all_dirs, all_files


"""
node_exporter-1.4.0.linux-amd64.tar.gz 下载地址 下载后放在当前目录
https://github.com/prometheus/node_exporter/releases/download/v1.4.0/node_exporter-1.4.0.linux-amd64.tar.gz
"""




def conn_linux(ip, port, username, password):
    ssh_client = paramiko.SSHClient()  # paramiko.client.SSHClient
    # 自动添加策略，保存服务器的主机名和密钥信息，如果不添加，那么不再本地know_hosts文件中记录的主机将无法连接 ，此方法必须放在connect方法的前面
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接SSH服务端，以用户名和密码进行认证 ，调用connect方法连接服务器
    ssh_client.connect(hostname=ip, port=port, username=username, password=password)
    return ssh_client


def close(ssh_client: SSHClient):
    if ssh_client:
        ssh_client.close()


def get_node_exporter():
    _, all_files = traverse_folder('.', True)
    for file in all_files:
        if os.path.basename(file).startswith('node_exporter'):
            print(f"找到了node_exporter安装包:{os.path.basename(file)}, 绝对路径:{file}")
            return file
    print("未找到node_exporter安装包, 去'https://github.com/prometheus/node_exporter/releases/download/v1.4.0/node_exporter"
          "-1.4.0.linux-amd64.tar.gz'下载后, 放在当前目录!!!")
    return None


def rm_and_create_folder(ssh_client: SSHClient, basename: str):
    cmd = f'rm -rf /etc/{basename}'
    _, stdout, stderr = ssh_client.exec_command(cmd)
    print(f"[{cmd}] stdout:{stdout.read().decode('utf-8')}")
    print(f"[{cmd}] stderr:{stderr.read().decode('utf-8')}")

    cmd = f'mkdir -p /etc/{basename}'
    _, stdout, stderr = ssh_client.exec_command(cmd)
    print(f"[{cmd}] stdout:{stdout.read().decode('utf-8')}")
    print(f"[{cmd}] stderr:{stderr.read().decode('utf-8')}")


def upload(ssh_client: SSHClient, upload_info: dict):
    sftp = ssh_client.open_sftp()
    for k, v in upload_info.items():
        ret = sftp.put(k, v)
        print(f"上传:{k}->{v} 结果:{ret}")
    sftp.close()


def decompressing(ssh_client: SSHClient, basename, filename):
    'tar -zxvf /etc/node_exporter-1.4.0.linux-amd64/node_exporter-1.4.0.linux-amd64.tar.gz -C /etc/node_exporter-1.4.0.linux-amd64/'
    cmd = f'tar -zxvf /etc/{basename}/{os.path.basename(filename)} -C /etc/{basename}/'
    _, stdout, stderr = ssh_client.exec_command(cmd)
    print(f"[{cmd}] stdout:{stdout.read().decode('utf-8')}")
    print(f"[{cmd}] stderr:{stderr.read().decode('utf-8')}")


def systemc_file(service_file, basename):
    content = f"""
[Unit]
Description=node_exporter
After=network.target
[Service]
Type=simple
User=root
ExecStart=/etc/{basename}/{basename}/node_exporter
Restart=always
[Install]
WantedBy=multi-user.target 
"""
    content = content.strip()
    with open(service_file, 'w', encoding='utf-8') as f:
        f.write(content)


def start_system(ssh_client: SSHClient, service_file: str):
    cmds = ["systemctl daemon-reload",
            f"systemctl start {service_file.replace('.service', '')}",
            f"systemctl enable {service_file.replace('.service', '')}",
            "systemctl start firewalld",
            "systemctl enable firewalld",
            "firewall-cmd --permanent --add-port=9100/tcp",
            "firewall-cmd --reload",
            "systemctl stop firewalld",
            "systemctl disable firewalld", ]
    for cmd in cmds:
        _, stdout, stderr = ssh_client.exec_command(cmd)
        print(f"[{cmd}] stdout:{stdout.read().decode('utf-8')}")
        print(f"[{cmd}] stderr:{stderr.read().decode('utf-8')}")


def main():
    ip = '172.17.140.17'
    port = 22
    username = 'root'
    password = 'abc123'
    ssh_client = conn_linux(ip, port, username, password)

    pkg = get_node_exporter()
    if not pkg:
        return
    basename = os.path.basename(pkg).replace('.tar.gz', '')
    print(f'node_exporter基础名称:{basename}')
    rm_and_create_folder(ssh_client, basename)

    service_file = 'node_exporter.service'
    node_exporter_file = f'/etc/systemd/system/{service_file}'
    systemc_file(service_file, basename)
    upload_info = {pkg: f'/etc/{basename}/{os.path.basename(pkg)}',
                   service_file: node_exporter_file}
    upload(ssh_client, upload_info)

    decompressing(ssh_client, basename, pkg)
    start_system(ssh_client, service_file)

    close(ssh_client)


if __name__ == '__main__':
    main()
```

### 3、安装git2.38

```sh
#git下载地址 https://mirrors.edge.kernel.org/pub/software/scm/git/
#去git地址查看版本.直接替换git_version可以安装任意版本
git_version=git-2.38
rm -rf /etc/${git_version}
mkdir -p /etc/${git_version}
yum remove -y git
yum install -y wget
wget -P /etc/${git_version} https://mirrors.edge.kernel.org/pub/software/scm/git/${git_version}.0.tar.gz --no-check-certificate
yum install -y curl-devel expat-devel openssl-devel gcc-c++
tar -zxvf /etc/${git_version}/${git_version}.0.tar.gz -C /etc/${git_version}
cd /etc/${git_version}/${git_version}.0
./configure --prefix=/usr/local/git
make -j8
make install -j8
echo "export PATH=$PATH:/usr/local/git/bin" >> /etc/profile
source /etc/profile
git --version
```

### 4、安装Prometheus2.39.1

```sh
base_folder=/etc/prometheus
mkdir -p $base_folder &&
cd $base_folder &&
yum install -y wget tar &&
wget https://github.com/prometheus/prometheus/releases/download/v2.39.1/prometheus-2.39.1.linux-amd64.tar.gz &&
tar -zxvf prometheus-2.39.1.linux-amd64.tar.gz &&
cat > /etc/systemd/system/prometheus.service << EOF &&
[Unit]
Description=Prometheus Service

[Service]
ExecStart=/etc/prometheus/prometheus-2.39.1.linux-amd64/prometheus --config.file=/etc/prometheus/prometheus-2.39.1.linux-amd64/prometheus.yml
Restart=always

[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload &&
systemctl start prometheus.service &&
systemctl enable prometheus.service &&
systemctl start firewalld &&
systemctl enable firewalld &&
firewall-cmd --permanent --add-port=9090/tcp &&
firewall-cmd --reload &&
systemctl stop firewalld &&
systemctl disable firewalld
```

### 5、安装go

Centos7 安装 go1.* 版本的golang
使用方法:
以go1.13.14.linux-amd64.tar.gz为例
把go1.13.14.linux-amd64.tar.gz放在当前目录, 没有就去'https://studygolang.com/dl'下载
先保证远程机器的SSH可用,然后配置文件中的四个字段
ip = '172.16.70.42'
port = 22
username = 'root'
password = '111111'
运行python3 install_go.py

```python
"""
https://studygolang.com/dl 下载go安装包的地址
"""

import os

import paramiko
from paramiko.client import SSHClient
from paramiko.ssh_exception import AuthenticationException


def traverse_folder(folder, only_first=False):
    folder = os.path.abspath(folder)
    all_files = []
    all_dirs = []
    if os.path.isdir(folder):
        for root, dirs, files in os.walk(folder):
            for one_file in files:
                all_files.append(os.path.join(root, one_file))  # 所有文件
            for one_dir in dirs:
                all_dirs.append(os.path.join(root, one_dir))  # 所有文件夹
            if only_first:
                break
    else:
        msg = 'Can not find folder:{} for traverse'.format(folder)
        print(msg)
    return all_dirs, all_files


def conn_linux(ip, port, username, password):
    ssh_client = paramiko.SSHClient()  # paramiko.client.SSHClient
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_client.connect(hostname=ip, port=port, username=username, password=password)
    except AuthenticationException as e:
        print("大概率是密码错误!!!!")
        raise e
    return ssh_client


def close(ssh_client: SSHClient):
    if ssh_client:
        ssh_client.close()


def get_pkg():
    _, all_files = traverse_folder('.', True)
    for file in all_files:
        if os.path.basename(file).startswith('go1.'):
            print(f"找到了go安装包:{os.path.basename(file)}, 绝对路径:{file}")
            return file
    raise Exception("未找到go安装包, 去'https://studygolang.com/dl'下载后, 放在当前目录!!!")


def exec_cmd(ssh_client: SSHClient, cmd):
    _, stdout, stderr = ssh_client.exec_command(cmd)
    print(f"[{cmd}] stdout:{stdout.read().decode('utf-8')}")
    print(f"[{cmd}] stderr:{stderr.read().decode('utf-8')}")


def rm_and_create_folder(ssh_client: SSHClient, linux_path: str):
    cmd = f'rm -rf {linux_path}'
    exec_cmd(ssh_client, cmd)

    cmd = f'mkdir -p {linux_path}'
    exec_cmd(ssh_client, cmd)


def upload(ssh_client: SSHClient, upload_info: dict):
    sftp = ssh_client.open_sftp()
    for k, v in upload_info.items():
        ret = sftp.put(k, v)
        print(f"上传:{k}->{v} 结果:{ret}")
    sftp.close()


def decompressing(ssh_client: SSHClient, linux_path, filename):
    cmd = f'tar -zxf {linux_path}/{os.path.basename(filename)} -C {linux_path}'
    _, stdout, stderr = ssh_client.exec_command(cmd)
    print(f"[{cmd}] stdout:{stdout.read().decode('utf-8')}")
    print(f"[{cmd}] stderr:{stderr.read().decode('utf-8')}")


def environment(ssh_client: SSHClient, linux_path):
    go_path = linux_path + '/go/bin'
    cmds = [f'echo "export PATH=$PATH:{go_path}" >> /etc/profile', 'source /etc/profile']
    for cmd in cmds:
        exec_cmd(ssh_client, cmd)


def go_env(ssh_client: SSHClient, linux_path):
    gopath = linux_path + '/go/bin/go'
    cmds = [f"{gopath} env -w GO111MODULE=on", f"{gopath} env -w GOPROXY=https://goproxy.cn,direct"]
    for cmd in cmds:
        exec_cmd(ssh_client, cmd)


def main():
    ip = '172.16.70.42'
    port = 22
    username = 'root'
    password = '111111'
    ssh_client = conn_linux(ip, port, username, password)

    pkg = get_pkg()
    basename = os.path.basename(pkg).replace('.tar.gz', '')
    print(f'go基础名称:{basename}')
    linux_path = f'/etc/{basename}'
    rm_and_create_folder(ssh_client, linux_path)

    upload_info = {pkg: f'{linux_path}/{os.path.basename(pkg)}'}
    upload(ssh_client, upload_info)

    decompressing(ssh_client, linux_path, pkg)
    environment(ssh_client, linux_path)
    go_env(ssh_client, linux_path)

    close(ssh_client)
    """
    若是已经登陆的机器需要先exit再重新登陆
    或者手动执行 source /etc/profile
    """


if __name__ == '__main__':
    """
    Centos7 安装 go1.* 版本的golang
    使用方法:
    以go1.13.14.linux-amd64.tar.gz为例
    把go1.13.14.linux-amd64.tar.gz放在当前目录, 没有就去'https://studygolang.com/dl'下载
    先保证远程机器的SSH可用,然后配置文件中的四个字段
    ip = '172.16.70.42'
    port = 22
    username = 'root'
    password = '111111'
    运行python3 install_go.py
    """
    main()
```

[github](https://github.com/rainbow-tan/learn-python/tree/main/Centos7%E4%B8%AA%E4%BA%BA%E8%84%9A%E6%9C%AC)