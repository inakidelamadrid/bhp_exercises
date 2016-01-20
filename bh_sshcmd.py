import paramiko  # pip install paramiko
import os


def ssh_command(ip, user, command):
    # you can run this script as
    # SSH_PRIV_KEY=[your private key path] python bh_sshcmd.py
    key = paramiko.RSAKey.from_private_key_file(os.getenv('SSH_PRIV_KEY'))

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    print "[==>connecting]"
    client.connect(ip, username=user, pkey=key)
    ssh_session = client.get_transport().open_session()

    if ssh_session.active:
        ssh_session.exec_command(command)
        print(ssh_session.recv(1024))
    return

ssh_command('127.0.0.1', 'ubuntu', 'id')
