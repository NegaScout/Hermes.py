from discord.ext.commands import Bot as BotBase
from discord import Intents
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from ipaddress import ip_network, ip_address
from asyncio import Lock
class Hermes(BotBase):

    def __init__(self, *args, **kwargs):

        # DISCORD
        self.token_path = "token"
        self.prefix = "+"
        self.guild = None
        self.ready = False
        self.cog_prefix = "src.cogs."

        # MISC
        self.scheduler = AsyncIOScheduler()

        # SQL
        self.DB_PATH = "data/database.db"
        self.DB_WIREGUARD_SCHEMA = "data/build.sql"
        self.db_conn = None
        self.cursor = None
        self.db_ready_future = None
        self.db_lock = Lock()
        
        # SSH
        self.SSH_CLIENT = None
        self.ssh_key_path = "hermes.key"
        self.known_hosts_file = "hermes_known_hosts"
        self.ssh_key = None
        self.ssh_pub_key = None
        self.ssh_port = 22
        self.ssh_username = 'user'#
        self.ssh_auth_timeout = 60

        # WIREGUARD
        self.wireguard_proxy_hostname = ip_address("192.168.122.142")
        self.wireguard_template_dir = "data/"
        self.wireguard_target_wg_conf = "/home/user/hermes.conf" #"/etc/wireguard/hermes.conf"
        self.wireguard_subnet = ip_network('10.0.0.0/27')
#        intents = Intents.default()
#        intents.message_content = True
        super().__init__(command_prefix=self.prefix,
                        intents=Intents.all(),
                        *args,
                        **kwargs)
        
    async def sync_tree(self):
        try:
            synced = await self.tree.sync()
            if synced:
                self.logger.info("Tree synced")
            else:
                self.logger.warning("Tree not synced!")
        except Exception as e:
            self.logger.warning(f"Could not sync tree!\n{e}")
            raise e

    def run(self):

        with open(self.token_path, "r") as token_fh:
            self.token = token_fh.read()
        self.start_logging()
        self.logger.info("###########################")
        self.logger.info("Hermess run")
        self.load_cogs()
        self.logger.info("Hermess run")
        super().run(self.token, reconnect=True)
    
    from src.Hermes.cogs import load_cogs
    from src.Hermes.logging import start_logging
    from src.Hermes.on_ import on_connect, on_disconnect, on_ready, on_message, on_error, on_command_error
    from src.Hermes.database import build_database \
                             ,ready_database \
                             ,wait_for_db_ready

    from src.Hermes.wireguard import insert_wireguard_user \
                             ,read_wireguard_users \
                             ,generate_wg_conf \
                             ,get_next_ip \
                             ,read_wireguard_ips \
                             ,user_in_database \
                             ,update_wireguard_conf

    from src.Hermes.paramiko import setup_paramiko \
                                    ,connect_params


    
