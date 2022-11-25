from loguru import logger


def log(action: str, message):
    logger.info("[{}] {}".format(action, message))
