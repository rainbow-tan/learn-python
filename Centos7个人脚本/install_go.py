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
