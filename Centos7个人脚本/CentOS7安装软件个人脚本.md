CentOS7安装软件个人脚本

# ①安装go

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
        if os.path.basename(file).startswith('go1.') and file.endswith('.tar.gz'):
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
    ip = '172.16.70.34'
    port = 22
    username = 'root'
    password = '123456'
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

# ②安装git

```
#git下载地址 https://mirrors.edge.kernel.org/pub/software/scm/git/
#去git地址查看版本.直接替换git_version可以安装任意版本
#https://mirrors.edge.kernel.org/pub/software/scm/git/git-2.10.4.tar.gz
#https://mirrors.edge.kernel.org/pub/software/scm/git/git-2.15.0.tar.gz
git_version=git-2.38.0
rm -rf /etc/${git_version}
mkdir -p /etc/${git_version}
yum remove -y git
yum install -y wget
wget -P /etc/${git_version} https://mirrors.edge.kernel.org/pub/software/scm/git/${git_version}.tar.gz --no-check-certificate
yum install -y curl-devel expat-devel openssl-devel gcc-c++
tar -zxvf /etc/${git_version}/${git_version}.tar.gz -C /etc/${git_version}
cd /etc/${git_version}/${git_version}
./configure --prefix=/usr/local/git
make -j8
make install -j8
echo "export PATH=$PATH:/usr/local/git/bin" >> /etc/profile
source /etc/profile
git --version
```

例如安装git-2.38.0，则设置git_version=git-2.38.0

![image-20230331101202080](https://img2023.cnblogs.com/blog/1768648/202303/1768648-20230331153034560-47516526.png)



# ③安装python

```python
#python下载地址 https://registry.npmmirror.com/binary.html?path=python/
#去python下载地址.直接替换version可以安装任意版本
#https://registry.npmmirror.com/-/binary/python/2.4.6/Python-2.4.6.tgz
#https://registry.npmmirror.com/-/binary/python/2.7/Python-2.7.tgz
#https://registry.npmmirror.com/-/binary/python/3.9.4/Python-3.9.4.tgz

version=3.9.4
python_version=python${version}
rm -rf /etc/${python_version}
mkdir -p /etc/${python_version}
yum install -y wget
wget -P /etc/${python_version} https://registry.npmmirror.com/-/binary/python/${version}/Python-${version}.tgz --no-check-certificate
yum install -y wget tar zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gcc make libffi-devel
tar -zxvf /etc/${python_version}/Python-${version}.tgz -C /etc/${python_version}
cd /etc/${python_version}/Python-${version}
./configure prefix=/usr/local/${python_version}
make -j8
make install -j8
if [ ${version:0:1} == "2" ]
then
  rm -rf /usr/bin/${python_version}
  ln -s /usr/local/${python_version}/bin/python /usr/bin/${python_version}
  rm -rf /usr/bin/python2
  ln -s /usr/local/${python_version}/bin/python /usr/bin/python2
  rm -rf /usr/bin/python
  ln -s /usr/local/${python_version}/bin/python /usr/bin/python
else
  rm -rf /usr/bin/${python_version}
  ln -s /usr/local/${python_version}/bin/python3 /usr/bin/${python_version}
  rm -rf /usr/bin/python3
  ln -s /usr/local/${python_version}/bin/python3 /usr/bin/python3
fi
#如果下载的是python2版本, 则软链接是python2 和 python 和 python${version}
#如果下载的是python3版本, 则软链接是python3 和 python${version}
```

# ④安装node_exporter

Centos7 安装 node exporter
使用方法:
以node_exporter-1.5.0.linux-amd64.tar.gz为例
把node_exporter-1.5.0.linux-amd64.tar.gz放在当前目录, 没有就去'https://prometheus.io/download/'下载
先保证远程机器的SSH可用,然后配置文件中的四个字段
ip = '172.16.70.42'
port = 22
username = 'root'
password = '111111'
运行python3 install_node_exporter.py

```sh
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


def conn_linux(ip, port, username, password):
    ssh_client = paramiko.SSHClient()  # paramiko.client.SSHClient
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip, port=port, username=username, password=password)
    return ssh_client


def close(ssh_client: SSHClient):
    if ssh_client:
        ssh_client.close()


def get_install_package(start_with):
    _, all_files = traverse_folder('.', True)
    for file in all_files:
        if os.path.basename(file).startswith(start_with) and os.path.basename(file).endswith(".tar.gz"):
            print(f"找到了'{start_with}'安装包:{os.path.basename(file)}, 绝对路径:{file}")
            return file
    msg = f"未找到'{start_with}'安装包, 去官网'https://prometheus.io/download/'下载后, 放在当前目录!!!"
    raise Exception(msg)


def rm_and_create_folder(ssh_client: SSHClient, basename: str):
    cmd = f'rm -rf /etc/{basename}'
    exec_cmd(ssh_client, cmd)

    cmd = f'mkdir -p /etc/{basename}'
    exec_cmd(ssh_client, cmd)


def upload(ssh_client: SSHClient, upload_info: dict):
    sftp = ssh_client.open_sftp()
    for k, v in upload_info.items():
        ret = sftp.put(k, v)
        print(f"上传:{k}->{v} 结果:{ret}")
    sftp.close()


def exec_cmd(ssh_client: SSHClient, cmd: str):
    _, stdout, stderr = ssh_client.exec_command(cmd)
    out = stdout.read().decode('utf-8')
    err = stderr.read().decode('utf-8')
    print(f"[{cmd}] stdout:{out}")
    print(f"[{cmd}] stderr:{err}")


def decompressing(ssh_client: SSHClient, basename, filename):
    cmd = f'tar -zxvf /etc/{basename}/{os.path.basename(filename)} -C /etc/{basename}/'
    exec_cmd(ssh_client, cmd)


def systemc_file(pre, service_file, basename):
    content = f"""
[Unit]
Description={pre}
After=network.target
[Service]
Type=simple
User=root
ExecStart=/etc/{basename}/{basename}/{pre}
Restart=on-failure
[Install]
WantedBy=multi-user.target 
"""
    content = content.strip()
    with open(service_file, 'w', encoding='utf-8') as f:
        f.write(content)


def start_system(ssh_client: SSHClient, pre: str, port: int):
    cmds = ["systemctl daemon-reload",
            f"systemctl start {pre}",
            f"systemctl enable {pre}",
            "systemctl start firewalld",
            "systemctl enable firewalld",
            f"firewall-cmd --permanent --add-port={port}/tcp",
            "firewall-cmd --reload",
            "systemctl stop firewalld",
            "systemctl disable firewalld", ]
    for cmd in cmds:
        exec_cmd(ssh_client, cmd)


def main():
    ip = '172.16.70.34'
    port = 22
    username = 'root'
    password = '123456'

    prefix = "node_exporter"
    server_port = 9100

    ssh_client = conn_linux(ip, port, username, password)

    pkg = get_install_package(prefix)
    if not pkg:
        return
    basename = os.path.basename(pkg).replace('.tar.gz', '')

    print(f'{prefix}基础名称:{basename}')
    rm_and_create_folder(ssh_client, basename)

    service_file = f'{prefix}.service'
    service_path = f'/etc/systemd/system/{service_file}'
    systemc_file(prefix, service_file, basename)
    upload_info = {pkg: f'/etc/{basename}/{os.path.basename(pkg)}',
                   service_file: service_path}
    upload(ssh_client, upload_info)

    decompressing(ssh_client, basename, pkg)
    start_system(ssh_client, prefix, server_port)

    close(ssh_client)


if __name__ == '__main__':
    main()
"""
    Centos7 安装 node exporter
    使用方法:
    以node_exporter-1.5.0.linux-amd64.tar.gz为例
    把node_exporter-1.5.0.linux-amd64.tar.gz放在当前目录, 没有就去'https://prometheus.io/download/'下载
    先保证远程机器的SSH可用,然后配置文件中的四个字段
    ip = '172.16.70.42'
    port = 22
    username = 'root'
    password = '111111'
    运行python3 install_node_exporter.py
"""
```

# ⑤安装Prometheus

使用方法:
以prometheus-2.37.0.linux-amd64.tar.gz为例
把prometheus-2.37.0.linux-amd64.tar.gz放在当前目录, 没有就去'https://prometheus.io/download/'下载
先保证远程机器的SSH可用,然后配置文件中的四个字段
ip = '172.16.70.42'
port = 22
username = 'root'
password = '111111'
运行python3 install_prometheus.py

```
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


def conn_linux(ip, port, username, password):
    ssh_client = paramiko.SSHClient()  # paramiko.client.SSHClient
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip, port=port, username=username, password=password)
    return ssh_client


def close(ssh_client: SSHClient):
    if ssh_client:
        ssh_client.close()


def get_install_package(start_with):
    _, all_files = traverse_folder('.', True)
    for file in all_files:
        if os.path.basename(file).startswith(start_with) and os.path.basename(file).endswith(".tar.gz"):
            print(f"找到了'{start_with}'安装包:{os.path.basename(file)}, 绝对路径:{file}")
            return file
    msg = f"未找到'{start_with}'安装包, 去官网'https://prometheus.io/download/'下载后, 放在当前目录!!!"
    raise Exception(msg)


def rm_and_create_folder(ssh_client: SSHClient, basename: str):
    cmd = f'rm -rf /etc/{basename}'
    exec_cmd(ssh_client, cmd)

    cmd = f'mkdir -p /etc/{basename}'
    exec_cmd(ssh_client, cmd)


def upload(ssh_client: SSHClient, upload_info: dict):
    sftp = ssh_client.open_sftp()
    for k, v in upload_info.items():
        ret = sftp.put(k, v)
        print(f"上传:{k}->{v} 结果:{ret}")
    sftp.close()


def exec_cmd(ssh_client: SSHClient, cmd: str):
    _, stdout, stderr = ssh_client.exec_command(cmd)
    out = stdout.read().decode('utf-8')
    err = stderr.read().decode('utf-8')
    print(f"[{cmd}] stdout:{out}")
    print(f"[{cmd}] stderr:{err}")


def decompressing(ssh_client: SSHClient, basename, filename):
    cmd = f'tar -zxvf /etc/{basename}/{os.path.basename(filename)} -C /etc/{basename}/'
    exec_cmd(ssh_client, cmd)


def systemc_file(pre, service_file, basename):
    content = f"""
[Unit]
Description={pre}
After=network.target
[Service]
Type=simple
User=root
ExecStart=/etc/{basename}/{basename}/{pre} --config.file=/etc/{basename}/{basename}/{pre}.yml
Restart=on-failure
[Install]
WantedBy=multi-user.target 
"""
    content = content.strip()
    with open(service_file, 'w', encoding='utf-8') as f:
        f.write(content)


def start_system(ssh_client: SSHClient, pre: str, port: int):
    cmds = ["systemctl daemon-reload",
            f"systemctl start {pre}",
            f"systemctl enable {pre}",
            "systemctl start firewalld",
            "systemctl enable firewalld",
            f"firewall-cmd --permanent --add-port={port}/tcp",
            "firewall-cmd --reload",
            "systemctl stop firewalld",
            "systemctl disable firewalld", ]
    for cmd in cmds:
        exec_cmd(ssh_client, cmd)


def main():
    ip = '172.16.70.34'
    port = 22
    username = 'root'
    password = '123456'

    prefix = "prometheus"
    server_port = 9090

    ssh_client = conn_linux(ip, port, username, password)

    pkg = get_install_package(prefix)
    if not pkg:
        return
    basename = os.path.basename(pkg).replace('.tar.gz', '')

    print(f'{prefix}基础名称:{basename}')
    rm_and_create_folder(ssh_client, basename)

    service_file = f'{prefix}.service'
    service_path = f'/etc/systemd/system/{service_file}'
    systemc_file(prefix, service_file, basename)
    upload_info = {pkg: f'/etc/{basename}/{os.path.basename(pkg)}',
                   service_file: service_path}
    upload(ssh_client, upload_info)

    decompressing(ssh_client, basename, pkg)
    start_system(ssh_client, prefix, server_port)

    close(ssh_client)


if __name__ == '__main__':
    main()
    """
    Centos7 安装 prometheus
    使用方法:
    以prometheus-2.37.0.linux-amd64.tar.gz为例
    把prometheus-2.37.0.linux-amd64.tar.gz放在当前目录, 没有就去'https://prometheus.io/download/'下载
    先保证远程机器的SSH可用,然后配置文件中的四个字段
    ip = '172.16.70.42'
    port = 22
    username = 'root'
    password = '111111'
    运行python3 install_prometheus.py
    """
```

[github](https://github.com/rainbow-tan/learn-python/tree/main/Centos7%E4%B8%AA%E4%BA%BA%E8%84%9A%E6%9C%AC)