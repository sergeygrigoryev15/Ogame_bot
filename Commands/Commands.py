import random
from datetime import timedelta

from Core.BaseEntity import BaseEntity
from Enums.FleetMissionTypes import FleetMissionTypes
from Enums.MenuTabs import MenuTabs
from Screens.FleetDestinationScreen import FleetDestinationScreen
from Screens.FleetMissionScreen import FleetMissionScreen
from Screens.FleetMovementsScreen import FleetMovementsScreen
from Screens.FleetScreen import FleetScreen
from Screens.GalaxyScreen import GalaxyScreen
from Screens.OverviewScreen import OverviewScreen


class Commands(BaseEntity):
    def save_fleet(self, planet):
        overview_screen = OverviewScreen()
        overview_screen.planets_list.select_planet(planet)
        planets = overview_screen.planets_list.data.keys()
        if len(planets) > 1:
            destination_planet = random.choice([p for p in planets if p is not planet])
        else:
            solar_system_planets = self.get_planets_in_my_system()
            destination_planet = solar_system_planets[
                0
            ].position  # if solar_system_planets else make expedition
        overview_screen.navigation_menu.open_tab(MenuTabs.FLEET)
        fleet_screen = FleetScreen()
        if fleet_screen.has_fleet:
            fleet_screen.select_all()
            fleet_screen.go_next()

            fleet_destination_screen = FleetDestinationScreen()
            fleet_destination_screen.select_speed(10)
            fleet_destination_screen.select_destination(destination_planet)
            fleet_destination_screen.go_next()

            fleet_mission_screen = FleetMissionScreen()
            fleet_mission_screen.select_mission_type()
            fleet_mission_screen.put_all_resources()
            fleet_mission_screen.send_fleet()

            self.notification_bot.send_message(
                f'fleet from planet {planet} was saved! (sent to {destination_planet}).'
            )
            self.db.return_fleet(planet)

            fleet_mission_screen.navigation_menu.open_tab(MenuTabs.OVERVIEW)
        else:
            self.notification_bot.send_message(
                f'There is no fleet on the planet {planet}. Nothing to save.'
            )
            fleet_screen.navigation_menu.open_tab(MenuTabs.OVERVIEW)

    def return_fleet(self):
        # TODO when saving fleet, remember time of sending ships.
        #  when returning fleet, return time will be current_time - time of sending.
        #  if return_time < N* enemy remaining_time, then return it
        planets = self.db.get_return_fleet_queue()
        overview_screen = OverviewScreen()
        log = overview_screen.fleetAlertsTab.get_log()
        enemy_fleets = filter(
            lambda el: el.is_friendly is False
            and el.mission_type == FleetMissionTypes.ATTACK,
            log,
        )
        for planet in [
            p
            for p in set(planets)
            if p
            not in [
                el.to_coordinates
                for el in enemy_fleets
                if el.remaining_time < timedelta(hours=1)
            ]
        ]:
            overview_screen.navigation_menu.open_tab(MenuTabs.FLEET_MOVEMENTS)
            fleet_movements_screen = FleetMovementsScreen()
            fleet_movements_screen.return_fleet(from_coordinates=planet)
            self.db.delete_returned_fleet(planet)
            self.notification_bot.send_message(f'Fleet returning to planet {planet}.')

    def get_planets_in_my_system(self):
        overview_screen = OverviewScreen()
        overview_screen.navigation_menu.open_tab(MenuTabs.GALAXY)
        galaxy_screen = GalaxyScreen()
        planets = galaxy_screen.get_planets()
        return list(
            filter(
                lambda planet: not any([planet.owner.on_vocations, planet.owner.admin]),
                planets,
            )
        )


commands = Commands()
