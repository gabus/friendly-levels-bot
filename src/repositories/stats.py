from psycopg import cursor


class Stats:

    def __init__(self, db: cursor):
        self.db = db

    def get_top_x_users(self, guild_id, limit):
        q = '''
            select q.member_id as member_id, 
            max(member_name) as member_name, 
            sum(message_count) as message_count, 
            sum(emoji_count) as emoji_count, 
            sum(voip_duration) as voip_duration,
            sum(message_count) * lw.message_weight as message_weighted,
            sum(emoji_count) * lw.reaction_weight  as reaction_weighted,
            sum(voip_duration) * lw.voip_weight  as voip_weighted,
            sum(message_count) * lw.message_weight + sum(emoji_count) * lw.reaction_weight + sum(voip_duration) * lw.voip_weight as total_weighted
            from (
            
                select distinct on (m.id) m.id as member_id, 
                m.name as member_name,
                count(mes.message) as message_count,
                0 as emoji_count,
                0 as voip_duration
                from members m 
                left join messages mes on mes.member_id = m.id 
                left join channels c on c.id = mes.channel_id 
                where c.guild_id = {guild_id}
                group by m.id, m.name
                
                union
                
                select distinct on (m.id) m.id as member_id, 
                m.name as member_name,
                0 as message_count,
                count(r.emoji) as emoji_count,
                0 as voip_duration
                from members m 
                left join reactions r on r.member_id = m.id 
                left join channels c on c.id = r.channel_id 
                where c.guild_id = {guild_id}
                group by m.id, m.name
                
                union
                
                select v.member_id as member_id, 
                max(m.name) as member_name, 
                0 as message_count,
                0 as emoji_count,
                sum(v.duration_time) as voip_duration
                from voip v 
                left join members m on m.id = v.member_id 
                where v.guild_id = {guild_id}
                group by v.member_id
                
            ) as q
            left join level_weights lw on lw.guild_id = {guild_id}
            group by q.member_id, lw.message_weight, lw.reaction_weight, lw.voip_weight
            order by total_weighted desc
            limit {limit}
            ;
        '''.format(guild_id=guild_id, limit=limit)

        self.db.execute(q)
        return self.db.fetchall()

    def get_my_stats(self, guild_id, member_id):
        # todo give back message_count, reaction_count, voip_in_s_count,
        #   rank position against everyone else
        return [{"me": "awesome"}]
