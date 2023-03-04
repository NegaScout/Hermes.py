from discord import ui, app_commands, TextStyle
from time import time
class WireguardModal(ui.Modal, title="Wireguard Configuration"):
    
    def __init__(self, bot):
        super().__init__()
        self.wg_pub_key = ui.TextInput(label = "Wireguard public key:")
        self.add_item(self.wg_pub_key)

    async def on_submit(self, interaction):
        self.bot.insert_wireguard_user(interaction.user.name,
                                       interaction.user.id,
                                       self.wg_pub_key)
        await interaction.response.defer()
    