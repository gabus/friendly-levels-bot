class Formatters:

    def __init__(self):
        self.medals = [':first_place:', ':second_place:', ':third_place:', ':military_medal:']
        self.metric_emoji = {'messages': ':keyboard:', 'reaction': ':hushed:', 'voip': ':microphone2:', 'playing': ':video_game:'}

    def top_stats(self, stats) -> str:

        response = ''
        place = 0

        for stat in stats:
            if place < 3:
                prize_emoji = self.medals[place]
                place += 1
            else:
                prize_emoji = self.medals[3]

            response += prize_emoji + ' ' + stat['member_name'] + '(Score ' + str(round(stat['total_weighted'])) + ')\n'
            response += '     ' + self.metric_emoji['messages'] + ' messages: ' + str(stat['message_count']) + '\n'
            response += '     ' + self.metric_emoji['reaction'] + ' emoji: '    + str(stat['emoji_count']) + '\n'
            response += '     ' + self.metric_emoji['voip']     + ' voip: '     + str(round(stat['voip_duration'] / 60)) + ' min \n'
            response += '     ' + self.metric_emoji['playing']  + ' playing: '  + str(round(stat['member_playing_duration'] / 60)) + ' min \n'
            response += '\n'

        return response
