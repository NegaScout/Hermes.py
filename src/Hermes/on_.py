async def on_connect(self):
    self.logger.info("Connected")

async def on_disconnect(self):
    self.logger.info("Disconnected")

async def on_ready(self):

    if not self.ready:
        self.ready = True
        self.logger.info("Hermes ready")
        self.stdout = self.get_channel(810599224718262304)
        self.guild = self.get_guild(716803899440234506)
        await self.ready_database()
        await self.build_database()
        await self.insert_wireguard_user(1, "pub", 2)
        await self.read_wireguard_users()
        try:
            await self.tree.sync(guild=self.guild) 
        except Exception as e:
            print(e)
    else:
        self.logger.info("Reconnected")

async def on_message(self, message):
    if not message.author.bot:#and message.author == self.get_user(309723713857650688)
        await self.process_commands(message)

#            await message.interaction.response.send_modal(WireguardModal())


async def on_error(self, err, *args, **kwargs):
    
    if err == "on_command_error":
        self.logger.debug("on_command_error Something went wrong.")
    else:
        raise exc.original

async def on_command_error(self, context, exception):

    if isinstance(exception, CommandNotFound):
        pass
    elif hassattr(exception, "original"):
        self.logger.debug(exception.original)
        raise exception.original
    else:
        self.logger.debug(exception)
        raise exception
