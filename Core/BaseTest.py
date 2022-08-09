import sys
import traceback
from Core.BaseEntity import BaseEntity
from Screens.BaseOgameScreen import BaseOgameScreen

from Screens.HubScreen import HubScreen
from Screens.LoginScreen import LoginScreen


class BaseTest(BaseEntity):
    def __init__(self):
        BaseEntity.__init__(self)

    def before(self) -> None:
        login_screen = LoginScreen()
        login_screen.login()
        hub_screen = HubScreen()
        hub_screen.continue_game()
        BaseOgameScreen.return_to_overview()

    def relogin(self) -> None:
        if HubScreen.is_open():
            hub_screen = HubScreen()
            hub_screen.continue_game()

    def reinitialize_browser(self):
        self.driver.get('chrome://settings/clearBrowserData')
        self.driver.get(self.url)
        self.sleep(5)

    def run_test(self) -> None:
        pass

    def finish(self) -> None:
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
