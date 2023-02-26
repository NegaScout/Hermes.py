from discord import ui, ButtonStyle

class WireguardMenu(ui.View):

    def __init__(self):
        super().__init__()
        self.value = None

    @ui.button(label="lAbEl",
                style=ButtonStyle.grey)
    async def menu(self, button, interaction):
        await interaction.response.send("lol")