from discord.ui import Button
from discord import ButtonStyle

"""
sync_tree docstring
"""


class DismissB(Button):
    """
    sync_tree docstring
    """

    def __init__(self, label, succes=True):
        super().__init__(label=label,
                         style=ButtonStyle.green if succes else ButtonStyle.red)

    async def callback(self, interaction):
        await interaction.response.defer()
        await interaction.delete_original_response()
