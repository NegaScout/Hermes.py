from os import path
from ansible_runner import Runner, RunnerConfig, run_async
from discord import app_commands
from discord.app_commands import Group
from src.UI.Views.Common import ActionOkV
"""
sync_tree docstring
"""


def ansible_init(self):
    """
    sync_tree docstring
    """
    config_predir = self.config['Ansible']
    self.ansible_private_dir = config_predir['ansible_private_dir']
    self.ansible_working_dir = config_predir['ansible_working_dir']
    self.ansible_setup_playbook = path.join(config_predir['ansible_working_dir'], config_predir['ansible_setup_playbook'])
    self.ansible_inventory = config_predir['ansible_inventory']
    self.ansible_roles = path.join(config_predir['ansible_working_dir'], 'roles')
    self.linode_runner = None
    self.ansible_passwd_template = config_predir["ansible_passwd_template"]
    self.ansible_command_group = AnsibleG(
        self, name="ansible", description="ansible module"
    )
    self.command_groups.append(self.ansible_command_group)

class AnsibleG(Group):
    """
    sync_tree docstring
    """

    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot

    @app_commands.command()
    @app_commands.checks.has_role('Hermes Admin')
    async def run(self, interaction):
        """
        sync_tree docstring
        """
        await interaction.response.defer()
        if self.bot.run_ansible():
            await interaction.followup.send(
                    view=ActionOkV(label="Ansible run"), ephemeral=True, silent=True
            )
        else:
            await interaction.followup.send(
                    view=ActionOkV(label="Could not run ansible", succes=False), ephemeral=True, silent=True
            )

def status_handler(status, runner_config=None):
    print(status)

def run_ansible(self):
    """
    sync_tree docstring
    """
    self.update_linode_data()
    if not self.linode_instance:
        return False
    ssh_user = 'root'
    if self.paramiko_try_user(self.ssh_username):
        ssh_user = self.ssh_username
    try:
        with open(path.join(self.ansible_private_dir, 'cmdline'), 'w') as inventory_fh:
            inventory_fh.write(f"-u {ssh_user}")#
        self.linode_runner = run_async(private_data_dir = self.ansible_private_dir,
                                       playbook = self.ansible_setup_playbook,
                                       inventory = self.ansible_inventory,
                                       roles_path = self.ansible_roles,
                                       quiet = True,
                                       status_handler= status_handler)
        print("ansible run")
        # Runner.event_handler -> na progress
        # Runner.finished_callback -> na end
    except Exception as e:
        print(e)
        return False
    return True
