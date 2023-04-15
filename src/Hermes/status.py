from tabulate import tabulate
from discord.app_commands import Group
from discord import app_commands
"""
sync_tree docstring
"""

def status_init(self):
    """
    sync_tree docstring
    """
#    config_predir = self.config["Linode"]
    self.linode_command_group = StatusG(
        self, name="status", description="status module"
    )
    self.command_groups.append(self.linode_command_group)
    self.status_callbacks = []
    self.status_accumulator = {}

def status_hup_handler(self):
    print("Status recieved hup")

# not used
#def register_status_callback(self, status):
#    """
#    sync_tree docstring
#    """
#    for key in status.keys():
#        if key not in self.status_accumulator:
#            self.status_accumulator[key] = [status[key]]
#        else:
#            self.status_accumulator[key].append(status[key])

class StatusG(Group):
    """
    sync_tree docstring
    """

    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot

    @app_commands.command()
    async def hermes(self, interaction):
        """
        sync_tree docstring
        """
        self.status_accumulator = {}
        for callback in self.bot.status_callbacks:
            status = await callback(self.bot)
            for key in status.keys():
                if key not in self.bot.status_accumulator:
                    self.bot.status_accumulator[key] = [status[key]]
                else:
                    self.bot.status_accumulator[key].append(status[key])
        status_table = tabulate(self.bot.status_accumulator, headers='keys')
        await interaction.response.send_message(content=f"```{ status_table }```", ephemeral=True, silent=True
            )
