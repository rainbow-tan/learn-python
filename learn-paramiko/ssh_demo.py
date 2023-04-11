import paramiko


def conn_by_password():
    """
    1)
    如果抛出异常:SSHException: Server '172.17.140.17' not found in known_hosts
    则需要设置ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    用来自动保存到ip到known_hosts文件中


    2)
    如果抛出异常:paramiko.ssh_exception.AuthenticationException: Authentication failed.
    则大概率是认证失败 用户名密码错误导致

    3)
    如果抛出异常:NoValidConnectionsError: [Errno None] Unable to connect to port 22 on 172.17.140.17
    则大概率是linux机器的sshd服务未启动
    """
    ssh = paramiko.SSHClient()
    ip = "172.17.140.17"
    port = 22
    username = "root"
    passwd = "abc123"
    timeout = 5
    # 自动保存IP到known_hosts文件中, 否则可能抛出异常
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port, username, passwd, timeout=timeout)
    print(f"连接成功:{ip}")
    return ssh
    # ssh.close()
    # print("关闭成功")


def conn_by_private_key():
    """
    1)
    如果抛出异常:SSHException: not a valid RSA private key file
    则给定的文件不是私钥文件


    2)
    如果抛出异常:paramiko.ssh_exception.AuthenticationException: Authentication failed.
    则大概率是认证失败 可能公钥没有放到Linux主机
    """
    ssh = paramiko.SSHClient()
    ip = "172.17.140.17"
    port = 22
    username = "root"
    filename = r"C:\Users\dell\.ssh\id_rsa"
    timeout = 5
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    key = paramiko.RSAKey.from_private_key_file(filename)
    ssh.connect(ip, port, username, pkey=key, timeout=timeout)
    print(f"连接成功:{ip}")
    return ssh
    # ssh.close()
    # print("关闭成功")


def exec_cmd(cmd: str, ssh: paramiko.SSHClient):
    cmd = cmd.strip()
    _, out, err = ssh.exec_command(cmd)
    out = out.read().decode()
    err = err.read().decode()
    return out, err


def main():
    # conn_by_password()
    ssh = conn_by_private_key()
    out, err = exec_cmd('ls -l', ssh)
    print(out)
    print("=" * 10)
    print(err)


if __name__ == '__main__':
    main()
