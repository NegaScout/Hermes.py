from discord.ext.commands import Bot as BotBase
from discord import Intents
from logging.handlers import RotatingFileHandler

from apscheduler.schedulers.asyncio import AsyncIOScheduler

class Hermes(BotBase):
    def __init__(self, *args, **kwargs):
        self.prefix = '$'
        self.guild = None
        self.scheduler = AsyncIOScheduler()
        self.ready = False
        intents = Intents.default()
        intents.message_content = True
        super().__init__(command_prefix = self.prefix,
                        intents=intents,
                        *args,
                        **kwargs)
    def run(self):


        with open("token", "r") as token_fh:
            self.token = token_fh.read()

        super().run(self.token, reconnect=True)

    async def on_connect(self):
        print("Connected")

    async def on_disconnect(self):
        print("Disconnected")
    
    async def on_ready(self):

        if not self.ready:
            self.ready = True
            self.guild = self.get_guild(716803899440234506)
            print("Hermes ready")
        else:
            print("Reconnected")
    
    async def on_message(self, message):
        pass


    def logging(self):

        self.logger = logging.getLogger('discord')
        logger.setLevel(logging.DEBUG)
        logging.getLogger('discord.http').setLevel(logging.INFO)
        
        handler = RotatingFileHandler(
                filename='discord.log',
                encoding='utf-8',
                maxBytes=32 * 1024 * 1024,  # 32 MiB
                backupCount=5,  # Rotate through 5 files
            )

        dt_fmt = '%Y-%m-%d %H:%M:%S'
        formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
        handler.setFormatter(formatter)
        logger.addHandler(handler)