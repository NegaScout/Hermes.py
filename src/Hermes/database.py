import os
from src.backend.sqlite import self_with_commit, scriptexec
from sqlite3 import connect

async def build_database(self):
    if os.path.isfile(self.DB_WIREGUARD_SCHEMA):
        try:
            scriptexec(self.cursor, self.DB_WIREGUARD_SCHEMA)
            self.db_conn.commit()
            self.logger.info("Database builded!")
        except Exception as e:
            self.logger.warn(f"Could not build database!\n{e}")

async def ready_database(self):
    try:
        self.db_conn = connect(self.DB_PATH, check_same_thread=False) if self.db_conn is None else None 
        self.cursor = self.db_conn.cursor() if self.cursor is None else None
        self.logger.info("Database initialized")
    except Exception as e:
        self.logger.warn(f"Database could not be initialized!\n{e}")