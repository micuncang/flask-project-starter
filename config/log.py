import logging
import os
import time
from logging.handlers import TimedRotatingFileHandler
from multiprocessing import Lock


class SafeTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, filename, when='h', interval=1, backupCount=0, encoding=None, delay=False, utc=False,
                 atTime=None):
        TimedRotatingFileHandler.__init__(
            self, filename, when, interval, backupCount, encoding, delay, utc, atTime)
        self.roll_over_lock = Lock()

    def doRollover(self):
        """
        do a rollover; in this case, a date/time stamp is appended to the filename
        when the rollover happens.  However, you want the file to be named for the
        start of the interval, not the current time.  If there is a backup count,
        then we have to get a list of matching filenames, sort them and remove
        the one with the oldest suffix.
        """
        if self.stream:
            self.stream.close()
            self.stream = None
        # get the time that this sequence started at and make it a TimeTuple
        currentTime = int(time.time())
        dstNow = time.localtime(currentTime)[-1]
        t = self.rolloverAt - self.interval
        if self.utc:
            timeTuple = time.gmtime(t)
        else:
            timeTuple = time.localtime(t)
            dstThen = timeTuple[-1]
            if dstNow != dstThen:
                if dstNow:
                    addend = 3600
                else:
                    addend = -3600
                timeTuple = time.localtime(t + addend)
        dfn = self.rotation_filename(self.baseFilename + "." +
                                     time.strftime(self.suffix, timeTuple))
        self.roll_over_lock.acquire()
        try:
            if not os.path.exists(dfn) and os.path.exists(self.baseFilename):
                os.rename(self.baseFilename, dfn)
        finally:
            self.roll_over_lock.release()
        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                os.remove(s)
        if not self.delay:
            self.stream = self._open()
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval
        # If DST changes and midnight or weekly rollover, adjust for this.
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            if dstNow != dstAtRollover:
                if not dstNow:  # DST kicks in before next rollover, so we need to deduct an hour
                    addend = -3600
                else:  # DST bows out before next rollover, so we need to add an hour
                    addend = 3600
                newRolloverAt += addend
        self.rolloverAt = newRolloverAt


class LogConfigLoader:
    @staticmethod
    def close_werkzeug_logger():
        logger = logging.getLogger('werkzeug')
        logger.setLevel(logging.ERROR)
        logger.disabled = True

    @staticmethod
    def load_flask_app_logger_config(log_file, backupCount=0):
        logger = logging.getLogger('flask.app')
        logger.setLevel('INFO')

        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(module)s: %(message)s')

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        time_file_handler = SafeTimedRotatingFileHandler(
            log_file, when='MIDNIGHT', backupCount=backupCount)
        time_file_handler.suffix = '%Y-%m-%d.log'
        time_file_handler.setFormatter(formatter)
        logger.addHandler(time_file_handler)

    @staticmethod
    def multiprocess_log_test_logger():
        logger = logging.getLogger('multilog_test')
        logger.setLevel('INFO')

        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(module)s: %(message)s')

        multiprocess_log_test_handler = SafeTimedRotatingFileHandler(
            "/tmp/multiprocess_log_test.log", when='S', interval=2, backupCount=0)
        multiprocess_log_test_handler.suffix = '%Y-%m-%d-%H-%M-%S.log'
        multiprocess_log_test_handler.setFormatter(formatter)

        if not len(logger.handlers):
            logger.addHandler(multiprocess_log_test_handler)

        return logger
