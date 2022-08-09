import random
from datetime import datetime

from Core.BaseEntity import BaseEntity
from Enums.FleetMissionTypes import FleetMissionTypes
from Enums.MenuTabs import MenuTabs
from Screens.SendFleetScreen import SendFleetScreen
from Screens.FleetMovementsScreen import FleetMovementsScreen
from Screens.FleetScreen import FleetScreen
from Screens.GalaxyScreen import GalaxyScreen
from Screens.OverviewScreen import OverviewScreen


class Commands(BaseEntity):
    def save_fleet(self, planet):
        """
        Send fleet with resources to other planet or to expedition if there only one planet.
        """
        overview_screen = OverviewScreen()
        overview_screen.planets_list.select_planet(planet)
        planets = overview_screen.planets_list.data.keys()
        if len(planets) > 1:
            destination_planet = random.choice([p for p in planets if p != planet])
            mission_type = FleetMissionTypes.TRANSPORT
        else:
            overview_screen.navigation_menu.open_tab(MenuTabs.GALAXY)
            galaxy_screen = GalaxyScreen()
            galaxy, solar_system = galaxy_screen.current_system
            destination_planet = [galaxy, solar_system, '16']
            mission_type = FleetMissionTypes.EXPEDITION
        overview_screen.navigation_menu.open_tab(MenuTabs.FLEET)
        fleet_screen = FleetScreen()
        if fleet_screen.has_fleet:
            fleet_screen.select_all()
            fleet_screen.go_next()

            send_fleet_screen = SendFleetScreen()
            send_fleet_screen.select_destination(destination_planet)
            send_fleet_screen.select_mission_type(mission_type)
            send_fleet_screen.select_speed(10)
            send_fleet_screen.put_all_resources()
            sending_datetime = send_fleet_screen.send_fleet()

            self.notification_bot.message_me(
                f'fleet from planet {planet} was saved! (sent to {destination_planet}).'
            )
            self.db.return_fleet(planet, sending_datetime)

            send_fleet_screen.navigation_menu.open_tab(MenuTabs.OVERVIEW)
        else:
            self.notification_bot.message_me(
                f'There is no fleet on the planet {planet}. Nothing to save.'
            )
            fleet_screen.navigation_menu.open_tab(MenuTabs.OVERVIEW)

    def return_fleet(self):
        """
        Get all planned fleets to return.
        If latest planned attack time is before planned fleet return time, then click return it.
        """
        planets = self.db.get_return_fleet_queue()
        overview_screen = OverviewScreen()
        log = overview_screen.fleetAlertsTab.get_log()
        enemy_fleets = filter(
            lambda el: el.is_friendly is False and el.mission_type == FleetMissionTypes.ATTACK, log,
        )
        enemy_targets = [enemy_fleet.to_planet for enemy_fleet in enemy_fleets]
        for planet in set(planets):
            fleet_flight_time = datetime.now() - self.db.get_return_fleet_sending_time(planet)
            fleet_return_time = datetime.now() + fleet_flight_time
            if planet in enemy_targets:
                attacks_times = [enemy_fleet.arrival_time for enemy_fleet in enemy_fleets
                                 if enemy_fleet.to_planet == planet]
                if max(attacks_times) > fleet_return_time:
                    continue
            overview_screen.navigation_menu.open_tab(MenuTabs.FLEET_MOVEMENTS)
            fleet_movements_screen = FleetMovementsScreen()
            fleet_movements_screen.return_fleet(from_coordinates=planet)
            self.db.delete_returned_fleet(planet)
            self.notification_bot.message_me(f'Fleet returning to planet {planet}.')


commands = Commands()
