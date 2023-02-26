from discord.ext.commands import Cog

class WireguardCog(Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_ready(self):
        print("Cog ready")
# ADD COMMAND FOR WG MODAL HERE
    
async def setup(bot):
    await bot.add_cog(WireguardCog(bot))

