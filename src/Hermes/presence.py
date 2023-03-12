from discord import Game, ActivityType
async def presence_starting(self):
    return None#Activity(name="Starting...", type=ActivityType.listening)
async def presence_on(self):
    return None#Activity(name="On!", type=ActivityType.listening)
async def presence_updating_db(self):
    return None#Activity(name="Updating database...", type=ActivityType.listening)
async def presence_updating_wg(self):
    return None#Activity(name="Updating gateway...", type=ActivityType.listening)
