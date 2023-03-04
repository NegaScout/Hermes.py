import paramiko

def setup_paramiko(self):
    try:
        self.SSH_CLIENT = paramiko.client.SSHClient()
        self.ssh_key = paramiko.ecdsakey.ECDSAKey(filename=self.ssh_key_path)
        self.SSH_CLIENT.set_missing_host_key_policy(paramiko.WarningPolicy())
        self.SSH_CLIENT.load_host_keys(self.known_hosts_file)
        self.SSH_CLIENT.set_log_channel('hermes')
        self.logger.info("Paramako configured!")
    except Exception as e:
        self.logger.warn(f"Paramako could not be configured!\n{e}")

def connect_params(self):
    args = self.ssh_hostname
    kwargs = {'port': self.ssh_port,
            'username': self.ssh_username,
            'pkey': self.ssh_key,
            'auth_timeout': self.ssh_auth_timeout
            } 
    return (args, kwargs)