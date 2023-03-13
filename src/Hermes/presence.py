from discord import Game, ActivityType

"""
sync_tree docstring
"""


async def presence_starting(self):
    """
    sync_tree docstring
    """
    return None  # Activity(name="Starting...", type=ActivityType.listening)


async def presence_on(self):
    """
    sync_tree docstring
    """
    return None  # Activity(name="On!", type=ActivityType.listening)


async def presence_updating_db(self):
    """
    sync_tree docstring
    """
    return None  # Activity(name="Updating database...", type=ActivityType.listening)


async def presence_updating_wg(self):
    """
    sync_tree docstring
    """
    return None  # Activity(name="Updating gateway...", type=ActivityType.listening)
