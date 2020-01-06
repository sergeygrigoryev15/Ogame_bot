import sys
import time
import traceback

from Bot.SlackChannels import SlackChannels
from Core.BaseTest import BaseTest


class BaseInfiniteTest(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.TIMEOUT = 60 * 2

    def main_loop(self):
        pass

    def __call__(self):
        iter = 1
        self.init()
        self.before()
        while True:
            print 'iteration = ', iter
            self.driver.refresh()
            self.relogin()
            try:
                self.main_loop()
            except Exception:
                self.slack_bot.send_message(traceback.format_exc(), channel=SlackChannels.ALERTS)
                traceback.print_exc(file=sys.stdout)
            print 'sleep {} seconds'.format(self.TIMEOUT)
            time.sleep(self.TIMEOUT)
            iter += 1
        self.finish()
