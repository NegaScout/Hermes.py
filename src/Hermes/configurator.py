import os
from configparser import ConfigParser

def configurator_init(self):

    self.config = ConfigParser(inline_comment_prefixes=('#'))
    config_prefix = 'config'

    self.config.read(os.path.join(config_prefix, 'config.ini'))
    config_dirs = os.listdir(config_prefix)
    
    for config_dir in config_dirs:
        path_ = os.path.join(config_prefix, config_dir, 'config.ini')
        if os.path.isfile(path_):
            self.config.read(path_)
