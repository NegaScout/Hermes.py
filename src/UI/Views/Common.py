from discord.ui import View
from src.UI.Buttons.Common import DismissB


"""
sync_tree docstring
"""

class ActionOkV(View):
    """
    sync_tree docstring
    """

    def __init__(self, label, succes=True):
        super().__init__()
        self.add_item(DismissB(label=label, succes=succes))