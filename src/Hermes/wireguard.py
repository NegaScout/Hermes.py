import jinja2
# maybe put to extension or module?
async def insert_wireguard_user(self, user_id:int, pub_key:str, date:int):
    statement = '''INSERT INTO WIREGUARD_USERS VALUES(?, ?, ?)''' 
    try:
        self.db_conn.execute(statement, (user_id, pub_key, date))
        self.logger.info(f"{(user_id, pub_key, date)} inserted into database.")
    except Exception as e:
        self.logger.warn(f"Could not insert to database!\n{e}")

async def read_wireguard_users(self):
    statement = '''SELECT * FROM WIREGUARD_USERS''' 
    try:
        temp = self.db_conn.execute(statement)
        return temp
        for row in self.cursor.fetchall():
            pass # parse
    except Exception as e:
        self.logger.warn(f"Could not read from database!\n{e}")

def generate_wg_conf(self, db_select_outpout):
    env = jinja2.Environment()
    template = env.get_template("Wireguard.conf")
    return template.render(HOST={}, PEERS={})

#atomicity..?
async def update_wireguard_conf(self):
    with self.SSH_CLIENT.connect():
        with self.SSH_CLIENT.open_sftp() as SFTP_conn:
            with SFTP_conn.file(self.wireguard_conf_path, mode='w') as wg_conf:
                entries = read_wireguard_users()
                wg_conf_string = generate_wg_conf(entries)
                wg_conf.write(wg_conf_string)