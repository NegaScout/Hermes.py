import asyncio, os
from discord.ext.commands import Bot as BotBase
from discord import Intents, ui, app_commands
from logging.handlers import RotatingFileHandler
from discord.ext.commands import CommandNotFound, command

from src.Embeds.Wireguard import WireguardMenu

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
#https://www.youtube.com/watch?v=4EIy0bw7s-s&list=PLYeOw6sTSy6ZGyygcbta7GcpI8a5-Cooc&index=5

from sqlite3 import connect
from src.backend.sqlite import with_commit, scriptexec


class Hermes(BotBase):

    def __init__(self, *args, **kwargs):

        self.prefix = "+"
        self.guild = None
        self.scheduler = AsyncIOScheduler()
        self.ready = False
        self.cog_prefix = "src.cogs."

        self.DB_PATH = "data/database.db"
        self.DB_WIREGUARD_SCHEMA = "data/build.sql"
        self.db_conn = None
        self.cursor = None
#        intents = Intents.default()
#        intents.message_content = True
        super().__init__(command_prefix=self.prefix,
                        intents=Intents.all(),
                        *args,
                        **kwargs)
        
    async def sync_tree(self):
        try:
            synced = await self.tree.sync()
            if synced:
                self.logger.info("Tree synced")
            else:
                self.logger.warning("Tree not synced!")
        except Exception as e:
            self.logger.warning(f"Could not sync tree!\n{e}")
            raise e

    def run(self):
        with open("token", "r") as token_fh:
            self.token = token_fh.read()
        self.start_logging()
        self.load_cogs()
        self.logger.info("Hermess run")
        super().run(self.token, reconnect=True)
    
    from src.Hermes.cogs import load_cogs
    from src.Hermes.logging import start_logging
    from src.Hermes.on_ import on_connect, on_disconnect, on_ready, on_message, on_error, on_command_error
    from src.Hermes.database import build_database \
                             ,ready_database

    from src.Hermes.wireguard import insert_wireguard_user \
                             ,read_wireguard_users


    
