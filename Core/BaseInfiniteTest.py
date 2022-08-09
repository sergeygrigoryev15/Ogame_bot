import sys
import time
import traceback

from Core.BaseTest import BaseTest

# TODO get rid of global variable
global stop_iterations
stop_iterations = False


class BaseInfiniteTest(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.TIMEOUT = 60 * 5

    def main_loop(self):
        pass

    def __call__(self):
        iteration = 1
        self.init()
        self.before()
        while True:
            self.logger.debug(f'iteration = {iteration}')
            self.relogin()
            try:
                self.main_loop()
            except Exception:
                self.notification_bot.message_me(traceback.format_exc(limit=1000))
                traceback.print_exc(file=sys.stdout)
            self.sleep(self.TIMEOUT)
            self.reinitialize_browser()
            iteration += 1
            global stop_iterations
            if stop_iterations:
                self.finish()
                stop_iterations = False
                break
