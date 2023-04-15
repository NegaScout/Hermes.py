import signal

def signals_init(self):

    def hup_handler(signum, frame):
        self.logger.info("Recieved HUP signal, reloading configuration...")
        for callback in self.hup_callbacks:
            callback()
    
    def term_handler(signum, frame):
        self.logger.info("Recieved TERM/INT signal, gracefully shutting down...")
        for callback in self.term_callbacks:
            callback()
        exit(0)

    self.hup_callbacks = []
    self.term_callbacks = []
    signal.signal(signal.SIGHUP, hup_handler)
    signal.signal(signal.SIGTERM, term_handler)
    signal.signal(signal.SIGINT, term_handler)
