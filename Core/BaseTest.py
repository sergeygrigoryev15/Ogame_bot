import sys
import traceback
from Core.BaseEntity import BaseEntity

from Screens.HubScreen import HubScreen
from Screens.LoginScreen import LoginScreen


class BaseTest(BaseEntity):

    def __init__(self):
        BaseEntity.__init__(self)

    def before(self):
        login_screen = LoginScreen()
        login_screen.login()
        hub_screen = HubScreen()
        hub_screen.continue_game()

    def relogin(self):
        try:
            hub_screen = HubScreen()
            hub_screen.continue_game()
        except Exception:
            pass

    def run_test(self):
        pass

    def finish(self):
        self.driver.quit()
        global web_driver
        web_driver = None

    def __call__(self):
        self.init()
        self.before()
        try:
            self.run_test()
        except Exception:
            traceback.print_exc(file=sys.stdout)
        finally:
            self.finish()
