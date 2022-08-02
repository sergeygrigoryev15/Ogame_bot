import sys
import time
import traceback

from Core.BaseTest import BaseTest


global stop
stop = False


class BaseInfiniteTest(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.TIMEOUT = 60 * 2

    def main_loop(self):
        pass

    def __call__(self):
        iteration = 1
        self.init()
        self.before()
        while True:
            self.logger.debug(f'iteration = {iteration}')
            self.driver.refresh()
            self.relogin()
            try:
                self.main_loop()
            except Exception:
                self.notification_bot.alert(traceback.format_exc())
                traceback.print_exc(file=sys.stdout)
            self.logger.debug(f'sleep {self.TIMEOUT} seconds')
            time.sleep(self.TIMEOUT)
            iteration += 1
            global stop
            if stop:
                self.finish()
