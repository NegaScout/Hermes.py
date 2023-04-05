import discord.app_commands.errors
from discord import Object
from discord.app_commands import CommandTree
"""
sync_tree docstring
"""

async def on_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError) -> None:
    if isinstance(error, app_commands.errors.CommandOnCooldown):
        await interaction.response.send_message(f'Command "{interaction.command.name}" is on cooldown, you can use it in {round(error.retry_after, 2)} seconds.', ephemeral=True)
    elif isinstance(error, app_commands.errors.MissingRole):
        await interaction.response.send_message(f'Command "{interaction.command.name}" requieres the {error.missing_role} role.', ephemeral=True)

async def on_connect(self):
    """
    sync_tree docstring
    """
    self.logger.info("Connected")


async def on_disconnect(self):
    """
    sync_tree docstring
    """
    self.logger.info("Disconnected")


async def on_ready(self):
    """
    sync_tree docstring
    """

    if not self.ready:
        self.ready = True
        self.stdout = self.get_channel(810599224718262304)
        self.guild = self.get_guild(716803899440234506)
        self.guild_snowflake = Object(716803899440234506)
        self.db_ready_future = self.ready_database()
        await self.db_ready_future

        for command in self.command_groups:
            self.tree.add_command(command)

        await self.sync_tree()
        self.logger.info("Hermes ready")
        # await self.change_presence(activity=self.presence_on())

    else:
        self.logger.info("Reconnected")


async def on_message(self, message):
    """
    sync_tree docstring
    """
    if not message.author.bot:
        await self.process_commands(message)
