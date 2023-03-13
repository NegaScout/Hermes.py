from logging import getLogger, Formatter, INFO, DEBUG
from logging.handlers import RotatingFileHandler

"""
sync_tree docstring
"""


def start_logging(self):
    """
    sync_tree docstring
    """
    self.logger = getLogger("hermes")
    self.logger.setLevel(INFO)
    discord_logger = getLogger("discord")
    discord_http_logger = getLogger("discord.http")
    discord_logger.setLevel(DEBUG)
    discord_http_logger.setLevel(INFO)
    handler = RotatingFileHandler(
        filename="discord.log",
        encoding="utf-8",
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,  # Rotate through 5 files
    )

    dt_fmt = "%Y-%m-%d %H:%M:%S"
    formatter = Formatter(
        "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
    )
    handler.setFormatter(formatter)
    self.logger.addHandler(handler)
    discord_logger.addHandler(handler)
    discord_http_logger.addHandler(handler)
