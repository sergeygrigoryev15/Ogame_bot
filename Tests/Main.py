from Core.BaseTest import BaseTest
from Elements.NavigationMenu import MenuTabs
from Screens.HubScreen import HubScreen
from Screens.LoginScreen import LoginScreen
from Screens.OverviewScreen import OverviewScreen


class Test(BaseTest):

    def run_test(self):
        login_screen = LoginScreen()
        login_screen.login()

        hub_screen = HubScreen()
        hub_screen.continue_game()

        overview_screen = OverviewScreen()
        print overview_screen.resources_tab.data
        overview_screen.navigation_menu.open_tab(MenuTabs.RESOURCES)
        print overview_screen.navigation_menu.active_tab
        print overview_screen.planets_list.active_planet
        print overview_screen.planets_list.data


if __name__ == '__main__':
    test = Test()
    test()
