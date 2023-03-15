import subprocess
from json import loads as json_loads
from ipaddress import ip_address
from discord.app_commands import Group
from discord import app_commands
from src.UI.Views.Common import ActionOkV
"""
sync_tree docstring
"""

def linode_init(self):
    """
    sync_tree docstring
    """
    config_predir = self.config["Linode"]
    self.linode_type = config_predir["linode_type"]
    self.linode_reagion = config_predir["linode_reagion"]
    self.linode_auth_users = config_predir["linode_auth_users"]
    self.linode_image = config_predir["linode_image"]
    self.linode_dns_ttl = config_predir.getint("linode_dns_ttl")
    self.linode_domain = config_predir["linode_domain"]
    self.linode_domain_id = None
    self.linode_record_id = None
    self.linode_ip = None
    self.linode_id = None
    self.linode_command_group = LinodeG(
        self, name="linode", description="linode module"
    )
    self.command_groups.append(self.linode_command_group)

class LinodeG(Group):
    """
    sync_tree docstring
    """

    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot

    @app_commands.command()
    async def deploy(self, interaction):
        """
        sync_tree docstring
        """
        await interaction.response.defer()
        if self.bot.create_linode():
            await interaction.followup.send(
                    view=ActionOkV(label="Linode deployed"), ephemeral=True, silent=True
            )
        else:
            await interaction.followup.send(
                    view=ActionOkV(label="Could not deploy", succes=False), ephemeral=True, silent=True
            )

    @app_commands.command()
    async def destroy(self, interaction):
        """
        sync_tree docstring
        """
        await interaction.response.defer()
        if self.bot.delete_linode():
            await interaction.followup.send(
                    view=ActionOkV(label="Linode destroyed"), ephemeral=True, silent=True
            )
        else:
            await interaction.followup.send(
                    view=ActionOkV(label="Could not destroy", succes=False), ephemeral=True, silent=True
            )

    @app_commands.command()
    async def fetch(self, interaction):
        """
        sync_tree docstring
        """
        await interaction.response.defer()
        self.bot.fetch_linodes()
        await interaction.followup.send(
                view=ActionOkV(label="Linode fetched"), ephemeral=True, silent=True
        )

def create_linode(self):
    """
    sync_tree docstring
    """
    if self.fetch_linodes():
        return False
    root_password = self.generate_password()
    linode_command = [
        "linode-cli",
        "linodes",
        "create",
        "--json",
        '--no-defaults',
        "--type",
        self.linode_type,
        "--region",
        self.linode_reagion,
        "--root_pass",
        root_password,
        "--authorized_users",
        self.linode_auth_users,
        '--image',
        self.linode_image,
        "--label",
        "wireguard"
    ]
    command = ' '.join(word for word in linode_command)
    proc = subprocess.run(command, shell=True, capture_output=True)
    response = json_loads(proc.stdout)[0]
    if not response.get("id", False):
        return False
    else:
        self.linode_ip = ip_address(response["ipv4"][0])
        self.linode_id = response["id"]
        return response

def fetch_linodes(self):
    """
    sync_tree docstring
    """
    linode_command = ["linode-cli", "linodes", "list", "--json"]
    command = ' '.join(word for word in linode_command)
    proc = subprocess.run(command, shell=True, capture_output=True)
    response = json_loads(proc.stdout)#[0]
    if not response:
        return False
    else:
        response = response[0]
        self.linode_ip = ip_address(response["ipv4"][0])
        self.linode_id = response["id"]
        return response

def delete_linode(self):
    """
    sync_tree docstring
    """
    if self.fetch_linodes():
        linode_command = ["linode-cli",
                          "linodes",
                          "delete",
                          "--json",
                          str(self.linode_id)]
        command = ' '.join(word for word in linode_command)
        proc = subprocess.run(command, shell=True, capture_output=True)
        return True
        
    return self.fetch_linodes()


def fetch_dns_records(self):
    """
    sync_tree docstring
    """
    linode_command = [
        "linode-cli",
        "domains",
        "records-list",
        "--json",
        self.linode_domain_id,
    ]

    proc = subprocess.run(linode_command, shell=True, capture_output=True)
    return json_loads(proc.stdout)


def add_dns_record(self, subdomain_name, ip):
    """
    sync_tree docstring
    """
    linode_command = [
        "linode-cli",
        "domains",
        "records-create",
        "--json",
        "--type",
        "A",
        "--ttl_sec",
        self.linode_dns_ttl,
        "--name",
        subdomain_name + "." + self.linode_domain,
        "--target",
        ip,
        self.linode_domain_id,
    ]
    proc = subprocess.run(linode_command, shell=True, capture_output=True)
    return json_loads(proc.stdout)


def delete_dns_record(self, linode_record_id):
    """
    sync_tree docstring
    """
    linode_command = [
        "linode-cli",
        "domains",
        "records-delete",
        self.linode_domain_id,
        linode_record_id,
    ]
    proc = subprocess.run(linode_command, shell=True, capture_output=True)
    return json_loads(proc.stdout)


# create response
# [{"id": 43564374,
# "label": "wireguard",
#  "group": "",
#   "status": "provisioning",
#    "created": "2023-03-08T18:20:42",
#     "updated": "2023-03-08T18:20:42",
#      "type": "g6-nanode-1",
#       "ipv4": ["192.46.235.117"],
#        "ipv6": "2a01:7e01::f03c:93ff:fe1e:5ff7/128",
#         "image": "linode/debian11",
#          "region": "eu-central",
#           "specs": {"disk": 25600,
#                     "memory": 1024,
#                      "vcpus": 1,
#                       "transfer": 1000},
#             "alerts": {"cpu": 90,
#                         "network_in": 10,
#                          "network_out": 10,
#                           "transfer_quota": 80,
#                            "io": 10000},
#             "backups": {"enabled": false,
#                         "available": false,
#                          "schedule": {"day": null, "window": null}, "last_successful": null}, "hypervisor": "kvm", "watchdog_enabled": true, "tags": [], "host_uuid": "a1ea5e93d29cfd4cdc6b2f50a8b63995bc780de5"}]

# [{"id": 43563961,
# "label": "linode43563961",
# "group": "",
# "status": "provisioning",
# "created": "2023-03-08T18:06:32",
# "updated": "2023-03-08T18:06:32",
# "type": "g6-nanode-1",
# "ipv4": ["172.104.130.22"],
# "ipv6": "2a01:7e01::f03c:93ff:fe1e:dc0d/128",
# "image": "linode/debian11", "region": "eu-central", "specs": {"disk": 25600, "memory": 1024, "vcpus": 1, "transfer": 1000}, "alerts": {"cpu": 90, "network_in": 10, "network_out": 10, "transfer_quota": 80, "io": 10000}, "backups": {"enabled": false, "available": false, "schedule": {"day": null, "window": null}, "last_successful": null}, "hypervisor": "kvm", "watchdog_enabled": true, "tags": [], "host_uuid": "6277e1d363191dbfd71e38409eba0d3e96f44fc9"}]
