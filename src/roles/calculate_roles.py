from src.repositories.repository import Repository
from discord.guild import Guild
from enum import Enum
from loguru import logger


class ChattingRoles(Enum):
    CHATTER_1 = "#1 Chatter"
    CHATTER_2 = "#2 Chatter"
    CHATTER_3 = "#3 Chatter"


class CalculateRoles:

    def __init__(self, db):
        self.repo = Repository(db)

    async def reassign_messages(self, guild: Guild):
        # todo issues:
        #   [] re assigning roles happen even if there are no new roles to re assign (happens with every message written)
        #   [] if roles are renamed, they won't be found
        #   [] these should be customisable by users and per Guild (saved in db roles (guild_id, chatter_1, chatter_2, chatter_3... etc))

        rows = self.repo.message.get_top_chatters(guild.id)
        logger.debug(rows)

        # collect all discord roles related to chatting
        c1_role = None
        c2_role = None
        c3_role = None
        for role in guild.roles:
            if role.name == ChattingRoles.CHATTER_1.value:
                c1_role = role
            if role.name == ChattingRoles.CHATTER_2.value:
                c2_role = role
            if role.name == ChattingRoles.CHATTER_3.value:
                c3_role = role

        # remove roles
        for member in guild.members:
            for member_role in member.roles:
                if member_role.name in [ChattingRoles.CHATTER_1.value, ChattingRoles.CHATTER_2.value, ChattingRoles.CHATTER_3.value]:
                    logger.debug("role removed for member: {}".format(member))
                    await member.remove_roles(*{c1_role, c2_role, c3_role}, reason="re-assigning roles")

        # add roles
        for member in guild.members:
            for row in rows:
                if member.id == row['member_id']:
                    new_role = None
                    if row['place'] == 1:
                        new_role = c1_role
                    if row['place'] == 2:
                        new_role = c2_role
                    if row['place'] == 3:
                        new_role = c3_role

                    logger.debug("assigning new role {}, to member: {}".format(new_role, member))

                    await member.add_roles(*{new_role}, reason="assigning new role")

    def calculate_reactions(self):
        pass

    def calculate_voip(self):
        pass

    def calculate_playing(self):
        pass

