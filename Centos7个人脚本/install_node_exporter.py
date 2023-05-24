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


def systemc_file(pre, service_file, basename,port):
    content = f"""
[Unit]
Description={pre}
After=network.target
[Service]
Type=simple
User=root
ExecStart=/etc/{basename}/{basename}/{pre} --web.listen-address=:{port}
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
    ip = '172.17.140.211'
    port = 22
    username = 'root'
    password = 'abc123'

    prefix = "node_exporter"
    server_port = 20001

    ssh_client = conn_linux(ip, port, username, password)

    pkg = get_install_package(prefix)
    if not pkg:
        return
    basename = os.path.basename(pkg).replace('.tar.gz', '')

    print(f'{prefix}基础名称:{basename}')
    rm_and_create_folder(ssh_client, basename)

    service_file = f'{prefix}.service'
    service_path = f'/etc/systemd/system/{service_file}'
    systemc_file(prefix, service_file, basename,server_port)
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