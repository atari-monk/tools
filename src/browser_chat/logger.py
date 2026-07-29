import logging


def create_logger(name: str="browser_chat"):

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger


    handler = logging.StreamHandler()


    formatter = logging.Formatter(
        "%(asctime)s "
        "%(levelname)s "
        "%(message)s"
    )


    handler.setFormatter(
        formatter
    )


    logger.addHandler(
        handler
    )


    logger.setLevel(
        logging.INFO
    )


    return logger