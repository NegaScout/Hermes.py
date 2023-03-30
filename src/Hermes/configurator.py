import os
from configparser import ConfigParser

"""
sync_tree docstring
"""


def configurator_init(self):
    """
    sync_tree docstring
    """

    self.config = ConfigParser(inline_comment_prefixes=("#",))
    self.config_prefix = "config"

    self.config.read(os.path.join(self.config_prefix, "config.ini"))
    config_dirs = os.listdir(self.config_prefix)
    for config_dir in config_dirs:
        path_ = os.path.join(self.config_prefix, config_dir, "config.ini")
        if os.path.isfile(path_):
            self.config.read(path_)
