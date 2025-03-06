import logging


def setup_logger(name:str) -> logging.Logger:
    """Sets up the logger for the class."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    # Adding handler to logger
    if not logger.handlers:
        logger.addHandler(ch)

    return logger