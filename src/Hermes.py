import logging, asyncio, os
from discord.ext.commands import Bot as BotBase
from discord import Intents, ui, app_commands
from logging.handlers import RotatingFileHandler
from discord.ext.commands import CommandNotFound, command

from src.Modals.Wireguard import WireguardModal

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
#https://www.youtube.com/watch?v=4EIy0bw7s-s&list=PLYeOw6sTSy6ZGyygcbta7GcpI8a5-Cooc&index=5
class Hermes(BotBase):

    def __init__(self, *args, **kwargs):

        self.prefix = '$'
        self.guild = None
        self.scheduler = AsyncIOScheduler()
        self.ready = False
        self.cog_prefix = "src.cogs."
#        intents = Intents.default()
#        intents.message_content = True
        super().__init__(command_prefix = self.prefix,
                                    intents=Intents.all(),
                                    *args,
                                    **kwargs)
        

    def load_cogs(self):
        cogs = os.listdir(self.cog_prefix.replace('.', '/'))
        cogs = map(self.cog_prefix.replace('.', '/').__add__, cogs) 
        cogs = filter(os.path.isfile, list(cogs))
        for cog in cogs:
            cog = cog[:-3].replace('/', '.')

            try:
                asyncio.run(self.load_extension(cog))
                self.logger.info(f"Cog {cog} loaded.")

            except Exception as e:
                self.logger.warning(f"Cog {cog} can not be loaded!")
                raise e

    def run(self):
        with open("token", "r") as token_fh:
            self.token = token_fh.read()
        self.start_logging()
        self.load_cogs()
        self.logger.info("Hermess run")
        super().run(self.token, reconnect=True)

    async def on_connect(self):
        self.logger.info("Connected")

    async def on_disconnect(self):
        self.logger.info("Disconnected")
    
    async def on_ready(self):

        if not self.ready:
            self.ready = True
            self.guild = self.get_guild(716803899440234506)
            self.logger.info("Hermes ready")
        else:
            self.logger.info("Reconnected")
    
    async def on_message(self, message):
        if not message.author.bot:
            print("got message")

    async def on_error(self, err, *args, **kwargs):
        
        if err == "on_command_error":
            await args[0].send("Something went wrong.")
        else:
            raise exc.original

    async def on_command_error(self, context, exception):

        if isinstance(exception, CommandNotFound):
            pass
        elif hassattr(exception, "original"):
            self.logger.debug(exception.original)
            raise exception.original
        else:
            self.logger.debug(exception)
            raise exception

    @command(name="wireguard")
    async def wg_modal(self, context):
        await context.send(embed=WireguardModal())

    def start_logging(self):
        self.logger = logging.getLogger('discord') # annother loggger for hermes?
        self.logger.setLevel(logging.DEBUG)
        logging.getLogger('discord.http').setLevel(logging.INFO) # is this enother logger?
        
        handler = RotatingFileHandler(
                filename='discord.log',
                encoding='utf-8',
                maxBytes=32 * 1024 * 1024,  # 32 MiB
                backupCount=5,  # Rotate through 5 files
            )

        dt_fmt = '%Y-%m-%d %H:%M:%S'
        formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
