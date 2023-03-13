from discord.ui import Button
from discord import ButtonStyle

"""
sync_tree docstring
"""


class DismissB(Button):
    """
    sync_tree docstring
    """

    def __init__(self):
        super().__init__(label="Ok", style=ButtonStyle.green)

    async def callback(self, interaction):
        await interaction.response.defer()
        await interaction.delete_original_response()
