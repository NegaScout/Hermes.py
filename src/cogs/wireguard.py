import discord
from discord.ext import commands

class Wireguard(commands.Cog)
    
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
    
#    @commands.command()
    
def setup(client):
    client.add_cog(Wireguard(client))

