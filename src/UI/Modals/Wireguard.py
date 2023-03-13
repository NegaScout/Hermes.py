from discord.ui import Modal, TextInput

"""
sync_tree docstring
"""


class WireguardSetupM(Modal, title="Wireguard Configuration"):
    """
    sync_tree docstring
    """

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.wg_pub_key = TextInput(label="Enter Wireguard public key:")
        self.add_item(self.wg_pub_key)

    async def on_submit(self, interaction):
        await self.bot.insert_wireguard_user(
            interaction.user.name, interaction.user.id, str(self.wg_pub_key)
        )
        await self.bot.update_wireguard_conf()
