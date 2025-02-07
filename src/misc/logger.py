import logging


def initialize_logger():
    fmt = "%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s: %(message)s"
    date_fmt = "%H:%M:%S"
    logging.basicConfig(
            level=logging.INFO,
            format=fmt, 
            datefmt=date_fmt)

    for lib in logging.Logger.manager.loggerDict.keys():
        logging.getLogger(lib).setLevel(logging.WARNING)

