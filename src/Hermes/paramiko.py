import paramiko

"""
sync_tree docstring
"""


def paramiko_init(self):
    """
    sync_tree docstring
    """
    config_predir = self.config["Paramiko"]
    self.ssh_key_path = config_predir["ssh_key_path"]
    self.known_hosts_file = config_predir["known_hosts_file"]
    self.ssh_port = int(config_predir["ssh_port"])
    self.ssh_username = config_predir["ssh_username"]
    self.ssh_auth_timeout = int(config_predir["ssh_auth_timeout"])
    self.SSH_CLIENT = None
    self.ssh_key = None
    self.ssh_pub_key = None


def setup_paramiko(self):
    """
    sync_tree docstring
    """
    try:
        self.SSH_CLIENT = paramiko.client.SSHClient()
        self.ssh_key = paramiko.ecdsakey.ECDSAKey(filename=self.ssh_key_path)
        self.SSH_CLIENT.set_missing_host_key_policy(
            paramiko.AutoAddPolicy()
        )  # paramiko.WarningPolicy()
        self.SSH_CLIENT.load_host_keys(self.known_hosts_file)
        self.SSH_CLIENT.set_log_channel("hermes")
        self.logger.info("Paramako configured!")
    except Exception as e:
        self.logger.warn(f"Paramako could not be configured!\n{e}")


def connect_params(self):
    """
    sync_tree docstring
    """
    args = self.wireguard_proxy_hostname
    kwargs = {
        "port": self.ssh_port,
        "username": self.ssh_username,
        "pkey": self.ssh_key,
        "auth_timeout": self.ssh_auth_timeout,
    }
    return (args, kwargs)
