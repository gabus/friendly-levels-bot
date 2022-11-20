from loguru import logger
from src.storage import StatsType


def log(guild_id: int, guild_name: str, member_id: int, member_name: str, action: StatsType, extra: str = None):
    logger.info("[{} {}] Member: {}({}) Guild: {}({})".format(action.value, extra or '', member_name, member_id, guild_name, guild_id))

