import jinja2
from src.backend.sqlite import self_with_commit
from time import time
from src.Hermes.database import wait_for_db_ready
from ipaddress import ip_network
from discord import Object as discordObject
from discord.app_commands import Group
from discord import app_commands
from src.UI.Modals.Wireguard import WireguardSetupM
from src.UI.Views.Wireguard import (
    WireguardAlreadyConfV,
    WireguardInstallV,
)

"""
sync_tree docstring
"""


def wireguard_init(self):
    """
    sync_tree docstring
    """
    config_predir = self.config["Wireguard"]
    self.wireguard_template_dir = config_predir["wireguard_template_dir"]
    self.wireguard_target_wg_conf = config_predir[
        "wireguard_target_wg_conf"
    ]  # "/etc/wireguard/hermes.conf"
    self.wireguard_subnet = ip_network(config_predir["wireguard_subnet"])
    self.wireguard_private_key_path = config_predir["wireguard_private_key_path"]
    self.wireguard_port = config_predir.getint("wireguard_port")
    self.PersistentKeepalive = config_predir.getint("PersistentKeepalive")
    self.wireguard_private_key = config_predir["wireguard_private_key"]
    self.wireguard_public_key = config_predir["wireguard_public_key"]
    self.wireguard_command_group = WireguardG(
        self, name="wireguard", description="Wireguard module"
    )


class WireguardG(Group):
    """
    sync_tree docstring
    """

    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot

    @app_commands.command()
    async def configure(self, interaction):
        """
        sync_tree docstring
        """
        if await self.bot.user_in_database(interaction.user.id):
            await interaction.response.send_message(
                content="You have already configured Wireguard.",
                view=WireguardAlreadyConfV(self.bot),
                ephemeral=True,
                silent=True,
            )
        else:
            await interaction.response.send_modal(WireguardSetupM(self.bot))

    @app_commands.command()
    async def help(self, interaction):
        """
        sync_tree docstring
        """

        if await self.bot.user_in_database(interaction.user.id):
            await interaction.response.send_message(
                view=WireguardInstallV(), ephemeral=True, silent=True
            )
        else:
            await interaction.response.send_modal(WireguardSetupM(self.bot))


async def load_wg_hermes_keys(self):
    """
    sync_tree docstring
    """

    if self.wireguard_private_key is not None:
        with open(self.wireguard_private_key_path, "r") as wg_key_fh:
            self.wireguard_private_key = wg_key_fh.read()

    if self.wireguard_public_key is not None:
        with open(self.wireguard_private_key_path + ".pub", "r") as wg_key_fh:
            self.wireguard_public_key = wg_key_fh.read()


async def user_in_database(self, user_id):
    """
    sync_tree docstring
    """
    users = await read_wireguard_users(self)
    return user_id in [user["USER_ID"] for user in users]


async def insert_wireguard_user(self, user_name: str, user_id: int, pub_key: str):
    """
    sync_tree docstring
    """
    statement = """INSERT INTO WIREGUARD_USERS (USER_ID, USER_NAME, PUB_KEY, USER_WG_IP, USER_WG_HOST_NUMBER, TIME_STAMP_REGISTERED) VALUES(?, ?, ?, ?, ?, ?) ON CONFLICT(user_id) DO UPDATE SET PUB_KEY = excluded.PUB_KEY, TIME_STAMP_REGISTERED = excluded.TIME_STAMP_REGISTERED"""
    # await self.change_presence(activity=self.presence_updating_db())
    if self.db_ready_future is not None:
        await self.db_ready_future
    next_ip_suffix = await self.get_next_ip()
    base_address = list(self.wireguard_subnet.hosts())[0]
    time_stamp = int(time())
    print(f"next ip suffix {next_ip_suffix}")
    try:
        async with self.db_lock:
            self.cursor.execute(
                statement,
                (
                    user_id,
                    user_name,
                    pub_key,
                    str(base_address + next_ip_suffix),
                    next_ip_suffix,
                    time_stamp,
                ),
            )
            self.db_conn.commit()
        self.logger.info(f"{(user_id, pub_key, time_stamp)} inserted into database.")
    except Exception as e:
        self.logger.warn(f"Could not insert to database!\n{e}")
    # await self.change_presence(activity=self.presence_on())


# @wait_for_db_ready
async def read_wireguard_users(self):
    """
    sync_tree docstring
    """
    statement = """SELECT * FROM WIREGUARD_USERS"""
    if self.db_ready_future is not None:
        await self.db_ready_future
    try:
        async with self.db_lock:
            self.cursor.execute(statement)
        return [dict(user) for user in self.cursor.fetchall()]
    except Exception as e:
        self.logger.error(f"Could not read from database!\n{e}")


async def read_wireguard_ips(self):
    """
    sync_tree docstring
    """
    statement = """SELECT * FROM WIREGUARD_USERS"""
    if self.db_ready_future is not None:
        await self.db_ready_future
    try:
        async with self.db_lock:
            self.cursor.execute(statement)
        ret = self.cursor.fetchall()
        return [dict(user)["USER_WG_HOST_NUMBER"] for user in self.cursor.fetchall()]
    except Exception as e:
        self.logger.error(f"Could not read from database!\n{e}")


# @wait_for_db_ready
async def get_next_ip(self):
    """
    sync_tree docstring
    """
    statement = """SELECT USER_WG_HOST_NUMBER FROM WIREGUARD_USERS"""
    if self.db_ready_future is not None:
        await self.db_ready_future
    try:
        async with self.db_lock:
            self.cursor.execute(statement)
        ret = await self.read_wireguard_ips()
        if not ret:
            ret = 1
        else:
            ret = sorted(ret)
            for i in range(len(ret)):
                if ret != i:
                    ret = i
                    break
            print(f"Not Fetching first: {ret}")

        self.logger.info(f"Fetched next ip = {ret} from database")
        return ret
    except Exception as e:
        self.logger.error(f"Could not read from database!\n{e}")


async def generate_wg_conf(self):
    """
    sync_tree docstring
    """
    fs_loader = jinja2.FileSystemLoader(self.wireguard_template_dir)
    env = jinja2.Environment(loader=fs_loader)
    template = env.get_template("Wireguard.conf")
    wg_users = await self.read_wireguard_users()

    host_config = {"Address": self.linode_ip, "PrivateKey": self.wireguard_private_key}

    misc = {"Endpoint": self.linode_ip, "ListenPort": self.wireguard_port}

    hermes = {
        "PUB_KEY": self.wireguard_public_key,
        "USER_WG_IP": list(self.wireguard_subnet.hosts())[0],
        "PersistentKeepalive": self.PersistentKeepalive,
    }

    return template.render(HOST=host_config, HERMES=hermes, PEERS=wg_users, MISC=misc)


async def update_wireguard_conf(self): # raise errors
    """
    sync_tree docstring
    """
    # args, kwargs = self.connect_params()
    # self.change_presence(activity=self.presence_updating_wg())
    with self.SSH_CLIENT:
        try:
            self.SSH_CLIENT.connect(
                str(self.linode_ip),
                port=self.ssh_port,
                username=self.ssh_username,
                pkey=self.ssh_key,
                auth_timeout=self.ssh_auth_timeout,
            )
        except Exception as e:
            self.logger.warn(f"Could not connect to {str(self.linode_ip)}")
        try:
            with self.SSH_CLIENT.open_sftp() as SFTP_conn:
                with SFTP_conn.file(self.wireguard_target_wg_conf, mode="w") as fh:
                    wg_conf_string = await self.generate_wg_conf()
                    fh.write(wg_conf_string)
            stdin, stdout, stderr = self.SSH_CLIENT.exec_command("ls -l")
        except Exception as e:
            self.logger.warn(f"Could not connect to {str(self.linode_ip)}")

    # await self.change_presence(activity=self.presence_on())
