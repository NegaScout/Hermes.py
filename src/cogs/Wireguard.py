from discord import Object as discordObject
from discord.ext.commands import Cog
from discord import app_commands
from src.Modals.Wireguard import WireguardSetupM, WireguardAlreadyConfV

"""
sync_tree docstring
"""


class WireguardCommand(Cog):
    """
    sync_tree docstring
    """

    def __init__(self, bot):
        self.bot = bot

    #    @Cog.listener()
    #    async def on_ready(self):
    #        pass

    @app_commands.command(name="wireguard_setup")
    async def wg_modal(self, interaction):
        """
        sync_tree docstring
        """

        if await self.bot.user_in_database(interaction.user.id):
            await interaction.response.send_message(
                content="You have already configured Wireguard.",
                view=WireguardAlreadyConfV(self.bot),
                ephemeral=True,
                silent=True,
            )
        else:
            await interaction.response.send_modal(WireguardSetupM(self.bot))


async def setup(bot):
    await bot.add_cog(WireguardCommand(bot))
