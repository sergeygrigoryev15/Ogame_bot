from datetime import timedelta

from Commands.Commands import commands
from Core.BaseInfiniteTest import BaseInfiniteTest
from Enums.FleetMissionTypes import FleetMissionTypes
from Screens.OverviewScreen import OverviewScreen


class SaveFleetTest(BaseInfiniteTest):
    SAVE_FLEET_TIMEOUT = timedelta(minutes=10)

    def main_loop(self):
        self.logger.debug('start loop')
        overview_screen = OverviewScreen()
        log = overview_screen.fleetAlertsTab.get_log()
        if log:
            self.logger.debug('log = ')
            self.logger.make_table(
                [el.__str__() for el in log], coloring={'is_friendly': lambda x: x}
            )
        enemy_fleets = [
            el for el in log if
            not el.is_friendly and
            el.mission_type == FleetMissionTypes.ATTACK and
            not el.is_return
        ]
        for fleet in enemy_fleets:
            if fleet.remaining_time < self.SAVE_FLEET_TIMEOUT:
                self.notification_bot.message_me(
                    f'we are under attack:\n{fleet.to_coordinates} ({fleet.remaining_time})'
                )
                commands.save_fleet(fleet.to_coordinates)
        commands.return_fleet()
        self.logger.debug('end loop')


if __name__ == '__main__':
    test = SaveFleetTest()
    test()
