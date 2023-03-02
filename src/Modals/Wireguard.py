from discord import ui, app_commands, TextStyle

class WireguardModal(ui.Modal, title = "Wireguard Configuration"):
    wg_pub_key = ui.TextInput(label = "Wireguard public key:")

    async def on_submit(self, interaction):
        print("WG MODAL INPUT: " + str(self.wg_pub_key))
        await interaction.response.defer()
    
    def insert_wireguard_user(db_conn, user_id:int, pub_key:str, date:int):
        statement = '''INSERT INTO WIREGUARD_USERS VALUES(?, ?, ?)''' 
        try:
            self.db_conn.execute((user_id, pub_key, date))
            self.logger.info(f"{(user_id, pub_key, date)} is inserted into wireguard users db.")
        except:
            self.logger.warn("Error when inserting into wg db!")
