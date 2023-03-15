from discord.ext.commands import Bot as BotBase
from discord import Intents
from apscheduler.schedulers.asyncio import AsyncIOScheduler

"""
Module docstring
"""


class Hermes(BotBase):

    """
    Hermes bot docstring
    """

    def __init__(self, *args, **kwargs):

        self.start_logging()
        self.logger.info("###########################")
        # CONFIGURATOR
        self.configurator_init()
        # DISCORD
        self.discord_init()
        # MISC
        self.scheduler = AsyncIOScheduler()
        # SQL
        self.database_init()
        # PARAMIKO
        self.paramiko_init()
        # WIREGUARD
        self.wireguard_init()
        # LINODE
        self.linode_init()

        super().__init__(
            command_prefix=self.prefix, intents=Intents.all(), *args, **kwargs
        )

    async def sync_tree(self):
        """
        sync_tree docstring
        """
        try:
            self.tree.copy_global_to(guild=self.guild_snowflake)
            synced = await self.tree.sync(guild=self.guild)  # guild=self.guild
            # print(await self.tree.fetch_commands(guild=self.guild))
            # print(synced)
            if synced:
                self.logger.info("Tree synced")
                print("Tree synced")
            else:
                self.logger.warning("Tree not synced!")
                print("Tree not synced!")
        except Exception as e:
            self.logger.warning(f"Could not sync tree!\n{e}")
            print("Could not sync tree!")
            raise e

    def run(self):
        """
        sync_tree docstring
        """
        self.logger.info("Hermess run")
        with open(self.token_path, "r") as token_fh:
            self.token = token_fh.read()

        # self.load_cogs()
        super().run(self.token, reconnect=True)

    from src.Hermes.configurator import configurator_init
    from src.Hermes.discord import discord_init
    from src.Hermes.cogs import load_cogs
    from src.Hermes.logging import start_logging
    from src.Hermes.on_ import (
        on_connect,
        on_disconnect,
        on_ready,
        on_message,
        on_error,
        on_command_error,
    )

    from src.Hermes.database import (
        database_init,
        build_database,
        ready_database,
        wait_for_db_ready,
    )

    from src.Hermes.wireguard import (
        wireguard_init,
        insert_wireguard_user,
        read_wireguard_users,
        generate_wg_conf,
        get_next_ip,
        read_wireguard_ips,
        user_in_database,
        update_wireguard_conf,
        load_wg_hermes_keys,
    )

    from src.Hermes.paramiko import paramiko_init, setup_paramiko, connect_params

    from src.Hermes.linode import (
        linode_init,
        fetch_linodes,
        create_linode,
        delete_linode,
        fetch_dns_records,
        add_dns_record,
        delete_dns_record,
    )

    from src.Hermes.presence import (
        presence_starting,
        presence_updating_db,
        presence_updating_wg,
        presence_on,
    )
    from src.Hermes.passwd import (
        generate_password
    )
