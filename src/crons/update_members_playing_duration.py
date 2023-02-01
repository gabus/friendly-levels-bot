from src.repositories.repository import Repository
from loguru import logger
import schedule
import time
import threading


class UpdateMembersPlayingDurationCron:

    def __init__(self, db):
        self.__repo = Repository(db)

    def __job(self):
        logger.debug("{}: updating member_playing_duration".format(self.__class__.__name__))
        self.__repo.member_playing.update_duration_time()
        logger.debug("{}: success".format(self.__class__.__name__))

    def __cron(self):
        schedule.every(1).minutes.do(self.__job)

        while 1:
            schedule.run_pending()
            time.sleep(1)

    def start(self):
        logger.debug("{}: is initialised".format(self.__class__.__name__))
        x = threading.Thread(target=self.__cron)
        x.start()
