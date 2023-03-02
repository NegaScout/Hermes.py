import os
import asyncio
def load_cogs(self):
    cogs = os.listdir(self.cog_prefix.replace('.', '/'))
    cogs = map(self.cog_prefix.replace('.', '/').__add__, cogs) 
    cogs = filter(os.path.isfile, list(cogs))
    for cog in cogs:
        cog = cog[:-3].replace('/', '.')
        try:
            asyncio.run(self.load_extension(cog))
            self.logger.info(f"Cog {cog} loaded.")
            print("cog loaded")

        except Exception as e:
            self.logger.warning(f"Cog {cog} can not be loaded!")
            raise e