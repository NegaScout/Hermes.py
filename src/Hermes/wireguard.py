import jinja2
from src.backend.sqlite import self_with_commit
from time import time
from src.Hermes.database import wait_for_db_ready
# maybe put to extension or module?
#@self_with_commit    
@wait_for_db_ready
async def insert_wireguard_user(self, user_name:str, user_id:int, pub_key:str):
    statement = '''INSERT INTO WIREGUARD_USERS VALUES(?, ?, ?, ?, ?)'''    
    next_ip_suffix = await self.get_next_ip()

    try:
        self.cursor.execute(statement, (user_name,
                                        user_id,
                                        pub_key,
                                        string(self.wireguard_subnet + next_ip_suffix),
                                        next_ip_suffix,
                                        int(time())))
        self.db_conn.commit()
        self.logger.info(f"{(user_id, pub_key, date)} inserted into database.")
    except Exception as e:
        self.logger.warn(f"Could not insert to database!\n{e}")

@wait_for_db_ready
async def read_wireguard_users(self):
    statement = '''SELECT * FROM WIREGUARD_USERS''' 
    try:
        self.cursor.execute(statement)
        return [dict(user) for user in self.cursor.fetchall()]
    except Exception as e:
        self.logger.error(f"Could not read from database!\n{e}")

@wait_for_db_ready
async def get_next_ip(self):
    statement = '''SELECT USER_WG_HOST_NUMBER FROM WIREGUARD_USERS'''
    try:
        self.cursor.execute(statement)
        ret = self.cursor.fetchall()
        print(ret)
        if not ret:
            ret = list(self.wireguard_subnet.hosts())[1]
        else:
            ret = sorted(ret)
            for i in range(len(ret)):
                if ret != i:
                    ret = i
                    break
        print(ret)
        self.logger.info(f"Fetched next ip = {ret} from database")
        return ret
    except Exception as e:
        self.logger.error(f"Could not read from database!\n{e}")

def generate_wg_conf(self):
    fs_loader = jinja2.FileSystemLoader(self.wireguard_template_dir)
    env = jinja2.Environment(loader=fs_loader)
    template = env.get_template("Wireguard.conf")
    wg_users = self.read_wireguard_users()
    for user in wg_users: 
        print(user)
    host_config = {'Address': self.wireguard_subnet.hosts()[0]}
    print(template.render(HOST={}, PEERS=wg_users, MISC={}))
    #return template.render(HOST={}, PEERS={})

#atomicity..?
async def update_wireguard_conf(self):
    connect_args, connect_kwargs = self.connect_params()
    with self.SSH_CLIENT.connect(*connect_args, **connect_kwargs):
        with self.SSH_CLIENT.open_sftp() as SFTP_conn:
            with SFTP_conn.file(self.wireguard_conf_path, mode='w') as wg_conf:
                entries = read_wireguard_users()
                wg_conf_string = generate_wg_conf(entries)
                wg_conf.write(wg_conf_string)