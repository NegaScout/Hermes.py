from discord.ui import Button
from discord import ButtonStyle
from src.UI.Modals.Wireguard import WireguardSetupM

"""
sync_tree docstring
"""


class WireguardReconfB(Button):
    """
    sync_tree docstring
    """

    def __init__(self, bot):
        super().__init__(label="Reconfigure", style=ButtonStyle.red)
        self.bot = bot

    async def callback(self, interaction):
        await interaction.response.send_modal(WireguardSetupM(self.bot))


class WireguardInstallB(Button):
    """
    sync_tree docstring
    """

    def __init__(self):
        super().__init__(
            label="Wireguard install page",
            style=ButtonStyle.link,
            url="https://www.wireguard.com/install/",
        )

    async def callback(self, interaction):
        await interaction.response.defer()
