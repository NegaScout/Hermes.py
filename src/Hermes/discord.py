def discord_init(self):
    config_predir = self.config['Discord']
    self.token_path = config_predir['token_path']
    self.prefix = config_predir['prefix']
    self.cog_prefix = config_predir['cog_prefix']
    self.guild = None
    self.ready = False