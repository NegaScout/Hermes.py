from discord import ui, app_commands, TextStyle

class WireguardModal(ui.Modal, title = "Wireguard Modal"):
    name = ui.TextInput(label = "name")
#    def __init__(self):
#        self.name = ui.TextInput(label = "name")
#        super().__init__()
#        self.add_item()

    async def on_submit(self, interaction):
        pass