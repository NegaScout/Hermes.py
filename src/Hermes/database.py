from os.path import isfile
from src.backend.sqlite import self_with_commit, scriptexec
from sqlite3 import connect, Row
from asyncio import sleep, get_event_loop

async def build_database(self):
    if isfile(self.DB_WIREGUARD_SCHEMA):
        try:
            scriptexec(self.cursor, self.DB_WIREGUARD_SCHEMA)
            self.db_conn.commit()
            self.logger.info("Database builded!")
        except Exception as e:
            self.logger.warn(f"Could not build database!\n{e}")

async def ready_database(self):
    try:
        if self.db_conn is None:
            self.db_conn = connect(self.DB_PATH, check_same_thread=False)
            self.db_conn.row_factory = Row
        
        self.cursor = self.db_conn.cursor() if self.cursor is None else None
        self.logger.info("Database initialized")
    except Exception as e:
        self.logger.warn(f"Database could not be initialized!\n{e}")
    await self.build_database()
    self.db_ready_future = None

def wait_for_db_ready(func):
    async def inner(*args, **kwargs):
        if args[0].db_ready_future is not None:
            await args[0].db_ready_future
        await func(*args, **kwargs)
    return inner

#async def wait_for_db_ready(self):
#    if self.db_ready_future is not None:
#        await self.db_ready_future
#    else:
#        await sleep(0)