import signal

def signals_init(self):

    def hup_handler(signum, frame):
        for callback in self.hup_callbacks:
            callback()
        self.logger.info("Recieved HUP")

    self.hup_callbacks = [self.status_hup_handler]
    signal.signal(signal.SIGHUP, hup_handler)
