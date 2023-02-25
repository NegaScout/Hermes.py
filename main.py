import discord, logging
from discord.ext import commands
from logging.handlers import RotatingFileHandler

logger = logging.getLogger('discord')
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

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix = '$', intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

wanted_extensions = ["wireguard"]

@client.command()
async def load(context, extension):
    client.load_extension(f"cogs.{extension}")

@client.command()
async def unload(context, extension):
    client.unload_extension(f"cogs.{extension}")

for extension in wanted_extensions:
    client.load_extension(f"cogs.{extension}")

token_fh = open("token", "r")
client.run(token_fh.read(), log_handler=None)
token_fh.close()
