from discord.ext.commands import Cog
from discord import app_commands, Object

class SyncTree(Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_ready(self):
        pass
    
    @app_commands.command(name="sync_tree")
    @app_commands.guilds(Object(id=716803899440234506))
    async def wg_modal(self, interaction):
        pass

async def setup(bot):
    await bot.add_cog(SyncTree(bot))

