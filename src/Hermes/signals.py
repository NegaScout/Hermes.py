import signal
import asyncio

def signals_init(self):

    self.hup_callbacks = []
    self.term_callbacks = []

def signals_init_async(self):

    loop = asyncio.get_event_loop()

    # needs to await in main loop
    async def hup_handler(signal_):
        self.logger.info("Recieved HUP signal, reloading configuration...")
        results = [await callback() for callback in self.hup_callbacks]
    
    async def term_handler(signal_):
        self.logger.info("Recieved TERM/INT signal, gracefully shutting down...")
        
        # wait for locks
        results = [await callback() for callback in self.term_callbacks]
        await self.close()
        exit(0)

    for signal_ in [signal.SIGINT, signal.SIGTERM]:
        loop.add_signal_handler(signal_, lambda: asyncio.create_task(term_handler(signal_)))
    
    loop.add_signal_handler(signal.SIGHUP, lambda: asyncio.create_task(hup_handler(signal_)))
    