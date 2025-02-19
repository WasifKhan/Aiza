import logging


class Logger:
    def __init__(self, level=logging.INFO):
        fmt = "%(asctime)s - %(filename)s:%(lineno)d " \
              "- %(levelname)s: %(message)s"
        date_fmt = "%H:%M:%S"
        for lib in logging.Logger.manager.loggerDict.keys():
            logging.getLogger(lib).setLevel(logging.WARNING)
        self.logger = logging.getLogger('__name__')
        self.logger.setLevel(level)
        formatter = logging.Formatter(fmt, datefmt=date_fmt)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def log(self, msg, level='INFO'):
        level = 10 if level == 'DEBUG' else 40 if level == 'ERROR' else 20
        self.logger.log(level=level, msg=msg)


logger = Logger()
