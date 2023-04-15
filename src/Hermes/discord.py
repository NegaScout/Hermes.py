"""
sync_tree docstring
"""


def discord_init(self):
    """
    sync_tree docstring
    """
    config_predir = self.config["Discord"]
    self.discord_token_path = config_predir["token_path"]
    self.cog_prefix = config_predir["cog_prefix"]
    self.guild = None
    self.ready = False
    self.command_groups = []
    with open(self.discord_token_path, "r") as token_fh:
        self.discord_token = token_fh.read()
