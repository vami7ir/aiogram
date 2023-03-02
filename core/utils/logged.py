import logging


def log():
    log_format = '%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'
    return logging.basicConfig(
        # filename="logfile.log",
        # filemode="+a",
        level=logging.INFO,
        format=log_format
    )
