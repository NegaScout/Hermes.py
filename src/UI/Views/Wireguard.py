from discord.ui import View
from src.UI.Buttons.Common import DismissB
from src.UI.Buttons.Wireguard import WireguardReconfB, WireguardInstallB


"""
sync_tree docstring
"""


class WireguardAlreadyConfV(View):
    """
    sync_tree docstring
    """

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.add_item(DismissB(label="Ok"))
        self.add_item(WireguardReconfB(self.bot))


class WireguardInstallV(View):
    """
    sync_tree docstring
    """

    def __init__(self):
        super().__init__()
        self.add_item(WireguardInstallB())
