from discord import ui, ButtonStyle, TextStyle
from time import time
class WireguardModal(ui.Modal, title="Wireguard Configuration"):
    
    def __init__(self, bot, from_view=False):
        super().__init__()
        self.bot = bot
        self.wg_pub_key = ui.TextInput(label = "Wireguard public key:")
        self.add_item(self.wg_pub_key)
        self.from_view = from_view

    async def on_submit(self, interaction):
        if not self.from_view and await self.bot.user_in_database(interaction.user.id):
            await interaction.response.send_message(view=WgOverwritePubkey(self.bot), ephemeral=True)
        else:
            await self.bot.insert_wireguard_user(interaction.user.name,
                                                 interaction.user.id,
                                                 str(self.wg_pub_key))
            if self.from_view:
                await interaction.response.edit_message(content="Updated") # delete_after=5.0 will be available in discord.py 2.2
            else:
                # send ephemeral in the channel
                await interaction.response.send_message(content="Configured.", ephemeral=True)
                #await interaction.response.defer()
            await self.bot.update_wireguard_conf() # stuck
            print(222)

class WgOverwritePubkey(ui.View):

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
    @ui.button(label="Enter new public key",
                style=ButtonStyle.green)
    async def menu(self, interaction, button):
        await interaction.response.send_modal(WireguardModal(self.bot, from_view=True))