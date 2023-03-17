from os import path
from ansible_runner import Runner, RunnerConfig
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
    self.ansible_working_dir = config_predir['ansible_working_dir']
    self.ansible_setup_role = config_predir['ansible_setup_role']
    self.ansible_config = 'ansible.cfg'
    self.ansible_inventory = 'inventory'
    ansible_env = {}
    ansible_env["ANSIBLE_CONFIG"] = path.join(self.ansible_working_dir, self.ansible_config)
    runner_options = {"private_data_dir": self.ansible_working_dir,
                      "project_dir": self.ansible_working_dir,
                      "playbook": path.join(self.ansible_working_dir, self.ansible_setup_role),
                      "envvars": ansible_env,
    }
    self.ansible_runner_config = RunnerConfig(**runner_options)
    self.ansible_runner_config.prepare()
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


def run_ansible(self):
    """
    sync_tree docstring
    """
    self.fetch_linodes()
    try:
        with open(path.join(self.ansible_working_dir, self.ansible_inventory), 'w') as inventory_fh:
            inventory_fh.write("[all]\n")
            inventory_fh.write(str(self.linode_ip))
        runner = Runner(config=self.ansible_runner_config)
        runner.run()
        # run async
        # cmdline_args -> změna z roota na hermes usera
        # Runner.event_handler -> na progress
        # Runner.finished_callback -> na end
    except Exception as e:
        print(e)
        return False
    return True
