from discord import ui, app_commands, TextStyle
class WireguardModal(ui.Modal, title = "Wireguard Modal"):
    public_key = ui.TextInput(label = "Put your publix key here",
                              style = TextStyle.short,
                              placeholder="Put your publix key here",
                              required = True,
                              max_length=64,
                              min_length = 40)
    async def on_submit(self, interaction):
        interaction.send("Cool") 