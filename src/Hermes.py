import logging, asyncio, os
from discord.ext.commands import Bot as BotBase
from discord import Intents, ui, app_commands
from logging.handlers import RotatingFileHandler
from discord.ext.commands import CommandNotFound, command

from src.Embeds.Wireguard import WireguardMenu

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
#https://www.youtube.com/watch?v=4EIy0bw7s-s&list=PLYeOw6sTSy6ZGyygcbta7GcpI8a5-Cooc&index=5
class Hermes(BotBase):

    def __init__(self, *args, **kwargs):

        self.prefix = "+"
        self.guild = None
        self.scheduler = AsyncIOScheduler()
        self.ready = False
        self.cog_prefix = "src.cogs."

#        intents = Intents.default()
#        intents.message_content = True
        super().__init__(command_prefix=self.prefix,
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
                print("cog loaded")

            except Exception as e:
                self.logger.warning(f"Cog {cog} can not be loaded!")
                raise e

    async def sync_tree(self):
        try:
            synced = await self.tree.sync()
            if synced:
                self.logger.info("Tree synced")
            else:
                self.logger.warning("Tree not synced!")
        except Exception as e:
            print(e)
            raise

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
            self.logger.info("Hermes ready")
            self.stdout = self.get_channel(810599224718262304)
            self.guild = self.get_guild(716803899440234506)
            try:
                await self.tree.sync(guild=self.guild) 
            except Exception as e:
                print(e)
            #await self.stdout.send("Hey", view=WireguardMenu())
        else:
            self.logger.info("Reconnected")
    
    async def on_message(self, message):
        if not message.author.bot:#and message.author == self.get_user(309723713857650688)
            await self.process_commands(message)

#            await message.interaction.response.send_modal(WireguardModal())


    async def on_error(self, err, *args, **kwargs):
        
        if err == "on_command_error":
            self.logger.debug("on_command_error Something went wrong.")
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
