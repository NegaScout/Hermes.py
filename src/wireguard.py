from discord.ext.commands import Cog

class WireguardCog(Cog):
    
    def __init__(self, bot):
        self.bot = bot
        print("Cog ready")
    
    @Cog.listener()
    async def on_ready(self):
        self.bot.info("??")
        print("Cog ready")
        print("Cog ready")
        print("Cog ready")
# ADD COMMAND FOR WG MODAL HERE
    
def setup(bot):
    print("Cog ready")
    bot.add_cog(Wireguard(bot))
    print("Cog ready")

