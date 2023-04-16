from os.path import join 
import jinja2
from linode_api4 import LinodeClient, Region, Domain, DomainRecord, Image, Type
from discord.app_commands import Group
from discord import app_commands
from src.UI.Views.Common import ActionOkV
from asyncio import Lock
"""
sync_tree docstring
"""

def linode_init(self):
    """
    sync_tree docstring
    """
    config_predir = self.config["Linode"]
    self.linode_token_path = join(self.config_prefix, "linode", "token")
    with open(self.linode_token_path, "r") as token_fh:
        self.linode_token = token_fh.read()
    self.linode_client = LinodeClient(self.linode_token)
    self.linode_type = Type(self.linode_client, config_predir["linode_type"])
    self.linode_region = Region(self.linode_client, config_predir["linode_region"])
    #self.linode_auth_users = User(self.linode_client, config_predir["linode_auth_users"])
    self.linode_image = Image(self.linode_client, config_predir["linode_image"])
    self.linode_domain_id = int(config_predir["linode_domain_id"])
    self.linode_domain = Domain(self.linode_client, self.linode_domain_id)
    self.linode_domain_records = {}
    self.linode_dns_ttl = config_predir.getint("linode_dns_ttl")
    self.linode_passwd_file = config_predir["linode_passwd_file"]
    self.linode_passwd = None
    self.linode_record_id = None
    self.linode_ip = None
    self.linode_instance = None
    self.linode_create_promise = None
    self.linode_lock = Lock()
    try:
        with open(config_predir["linode_wireguard_private_key"], "r") as wg_key_fh:
            self.linode_wireguard_private_key = wg_key_fh.read()
    except OSError as e:
        print(e)
    try:
        with open(config_predir["linode_wireguard_private_key"] + ".pub", "r") as wg_key_fh:
            self.linode_wireguard_public_key = wg_key_fh.read()
    except OSError as e:
        print(e)

    self.linode_command_group = LinodeG(
        self, name="linode", description="linode module"
    )
    self.command_groups.append(self.linode_command_group)
    async def linode_terminate_handler():
        await self.linode_lock.acquire()
    self.term_callbacks.append(linode_terminate_handler) # todo make macro
    
    self.status_callbacks.append(linode_status)

async def linode_status(self):
    self.update_linode_data()
    if not self.linode_instance:
        status = 'Off'
    else:
        status = self.linode_instance.__dict__['status']
    return {'Service': 'Linode', 'Domain': '', 'Status': status}

class LinodeG(Group):
    """
    sync_tree docstring
    """

    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot

    @app_commands.command()
    @app_commands.checks.has_role('Hermes Admin')
    async def deploy(self, interaction):
        """
        sync_tree docstring
        """
        ret = await self.bot.create_linode(interaction)
        if ret:
            ret = await self.bot.add_dns_record('minecraft', self.bot.linode_instance.__dict__['ipv4'][0])
            ret = await self.bot.add_dns_record('wireguard', self.bot.linode_instance.__dict__['ipv4'][0])
        return ret

    @app_commands.command()
    @app_commands.checks.has_role('Hermes Admin')
    async def destroy(self, interaction):
        """
        sync_tree docstring
        """
        ret = await self.bot.delete_linode(interaction)
        if ret:
            ret = await self.bot.delete_dns_record('wireguard')
            ret = await self.bot.delete_dns_record('minecraft')
        return ret

async def record_delete(self, interaction):
    """
    sync_tree docstring
    """
    linode_instances = self.linode_client.linode.instances()
    if linode_instances:
        self.linode_instance = linode_instances[0]
    else:
        self.linode_instance = None
        await interaction.response.send_message(
                view=ActionOkV(label="No active linode", succes=False), ephemeral=True, silent=True
        )
        return

    await self.delete_dns_record('wireguard')
    await self.delete_dns_record('minecraft')

    await interaction.response.send_message(
            view=ActionOkV(label="Record deleted", succes=True), ephemeral=True, silent=True
    )

async def record_add(self, interaction):
    """
    sync_tree docstring
    """
    self.update_linode_data()
    if not self.linode_instance:
        await interaction.response.send_message(
                view=ActionOkV(label="No active linode", succes=False), ephemeral=True, silent=True
        )
        return
    
    
    
    if not ret:
        await interaction.response.send_message(
                view=ActionOkV(label="Record already present", succes=True), ephemeral=True, silent=True
        )
    else:
        await interaction.response.send_message(
                view=ActionOkV(label="Record created", succes=True), ephemeral=True, silent=True
        )

async def create_linode(self, interaction):
    """
    sync_tree docstring
    """
    await interaction.response.defer()
    self.update_linode_data()
    
    if not self.linode_instance:
        id_ = interaction.id

        self.linode_instance, self.linode_passwd = self.linode_client.linode.instance_create(self.linode_type,
                                                                        self.linode_region,
                                                                        image=self.linode_image,
                                                                        label='wireguard',
                                                                        authorized_keys=[self.ssh_key_path + '.pub', '/home/honza/.ssh/id_ed25519.pub'])
        self.linode_ip = self.linode_instance.__dict__['ipv4'][0]
        fs_loader = jinja2.FileSystemLoader('config/ansible')
        env = jinja2.Environment(loader=fs_loader)
        template = env.get_template(self.ansible_passwd_template)
        passwd_jinja = template.render(passwd=self.linode_passwd)

        with open(join(self.ansible_private_dir, 'passwords'), 'w') as inventory_fh:
            inventory_fh.write(passwd_jinja)

        with open(self.ansible_inventory, 'w') as inventory_fh:
            inventory_fh.write("[all]\n")
            inventory_fh.write(str(self.linode_ip))
        
        await interaction.followup.send(
                view=ActionOkV(label="Linode deployed"), ephemeral=True, silent=True
        )
        with open(self.linode_passwd_file, 'w') as password_fh:
            password_fh.write(self.linode_passwd)

        return True
    elif self.linode_instance:
        await interaction.followup.send(
                view=ActionOkV(label="Linode already deployed", succes=True), ephemeral=True, silent=True
            )

async def delete_linode(self, interaction):
    """
    sync_tree docstring
    """
    await interaction.response.defer()
    self.update_linode_data()

    if self.linode_instance:
        self.linode_instance.delete()
        self.linode_instance = None
    else:
        await interaction.followup.send(
                view=ActionOkV(label="Linode already destroyed"), ephemeral=True, silent=True
        )
        return
    linode_instances = self.linode_client.linode.instances()
    
    if not linode_instances:
        await interaction.followup.send(
                view=ActionOkV(label="Linode destroyed"), ephemeral=True, silent=True
        )
    elif linode_instances:
        await interaction.followup.send(
                view=ActionOkV(label="Could not destroy", succes=False), ephemeral=True, silent=True
        )

async def add_dns_record(self, record_name, ip):
    """
    sync_tree docstring
    """
    record = self.linode_domain.record_create('A',
                                            id=self.linode_domain_id,
                                                name=record_name,
                                                target=ip)
    self.linode_domain_records[record_name] = record
    return True

async def delete_dns_record(self, record_name):
    """
    sync_tree docstring
    """
    ret = False
    for record in self.linode_domain.records:
        if record.name == record_name:
            record.delete()
            ret = True
    return ret

def update_linode_data(self):
    linode_instances = self.linode_client.linode.instances()
    if linode_instances:
        self.linode_instance = linode_instances[0]
        self.linode_ip = self.linode_instance.__dict__['ipv4'][0]
    else:
        self.linode_instance = None
        self.linode_ip = None
