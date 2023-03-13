from os.path import isfile
from sqlite3 import connect, Row
from asyncio import Lock
from src.backend.sqlite import scriptexec

"""
sync_tree docstring
"""


def database_init(self):
    """
    sync_tree docstring
    """

    config_predir = self.config["Database"]
    self.DB_PATH = config_predir["DB_PATH"]
    self.DB_WIREGUARD_SCHEMA = config_predir["DB_WIREGUARD_SCHEMA"]
    self.db_conn = None
    self.cursor = None
    self.db_ready_future = None
    self.db_lock = Lock()


async def build_database(self):
    """
    sync_tree docstring
    """

    if isfile(self.DB_WIREGUARD_SCHEMA):
        try:
            scriptexec(self.cursor, self.DB_WIREGUARD_SCHEMA)
            self.db_conn.commit()
            self.logger.info("Database builded!")
        except Exception as e:
            self.logger.warn(f"Could not build database!\n{e}")
    else:
        pass
        # raise WG SCHEMA NOT FOUND


async def ready_database(self):
    """
    sync_tree docstring
    """
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
    """
    sync_tree docstring
    """

    async def inner(*args, **kwargs):
        if args[0].db_ready_future is not None:
            await args[0].db_ready_future
        await func(*args, **kwargs)

    return inner


# async def wait_for_db_ready(self):
#    if self.db_ready_future is not None:
#        await self.db_ready_future
#    else:
#        await sleep(0)
