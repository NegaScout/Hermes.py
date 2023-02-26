from discord import Permissions
class Hermes(Permissions):

    def __init__(self, *args, **kwargs):

        super().__init__(**kwargs)
