import random

from Core.BaseEntity import BaseEntity
from Enums.MenuTabs import MenuTabs
from Screens.FleetDestinationScreen import FleetDestinationScreen
from Screens.FleetMissionScreen import FleetMissionScreen
from Screens.FleetMovementsScreen import FleetMovementsScreen
from Screens.FleetScreen import FleetScreen
from Screens.OverviewScreen import OverviewScreen


class Commands(BaseEntity):

    def save_fleet(self, planet):
        overview_screen = OverviewScreen()
        overview_screen.planets_list.select_planet(planet)
        overview_screen.navigation_menu.open_tab(MenuTabs.FLEET)
        fleet_screen = FleetScreen()
        if fleet_screen.has_fleet:
            fleet_screen.select_all()
            fleet_screen.go_next()

            fleet_destination_screen = FleetDestinationScreen()
            fleet_destination_screen.select_speed(10)
            planets = fleet_destination_screen.planets_list.data.keys()
            destination_planet = random.choice([p for p in planets if p is not planet])
            fleet_destination_screen.select_destination(destination_planet)
            fleet_destination_screen.go_next()

            fleet_mission_screen = FleetMissionScreen()
            fleet_mission_screen.select_mission_type()
            fleet_mission_screen.put_all_resources()
            fleet_mission_screen.send_fleet()

            self.slack_bot\
                .send_message('fleet from planet {} was saved! (sent to {}).'.format(planet, destination_planet))
            # add fleet to database

            fleet_mission_screen.navigation_menu.open_tab(MenuTabs.OVERVIEW)
        else:
            self.slack_bot.send_message('There is no fleet on the planet {}. Nothing to save.'.format(planet))
            fleet_screen.navigation_menu.open_tab(MenuTabs.OVERVIEW)

    def return_fleet(self, planet):
        overview_screen = OverviewScreen()
        if not overview_screen.fleetAlertsTab.is_alert:
            overview_screen.navigation_menu.open_tab(MenuTabs.FLEET_MOVEMENTS)
            fleet_movements_screen = FleetMovementsScreen()
            fleet_movements_screen.return_fleet(from_coordinates=planet)
            # delete task from queue
            self.slack_bot.send_message('Fleet returning to planet {}.'.format(planet))


commands = Commands()
