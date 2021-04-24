from datetime import timedelta

from Bot.SlackChannels import SlackChannels
from Commands.Commands import commands
from Core.BaseInfiniteTest import BaseInfiniteTest
from Enums.FleetMissionTypes import FleetMissionTypes
from Screens.OverviewScreen import OverviewScreen


class Test(BaseInfiniteTest):

    SAVE_FLEET_TIMEOUT = timedelta(minutes=10)

    def main_loop(self):
        self.logger.debug('start loop')
        overview_screen = OverviewScreen()
        log = overview_screen.fleetAlertsTab.get_log()
        if log:
            self.logger.debug('log = ')
            self.logger.make_table([el.__str__() for el in log], coloring={'is_friendly': lambda x: x})
        for fleet in [el for el in log if el.is_friendly and not el.is_return]:
            self.db.return_fleet(fleet.from_coordinates)
        commands.return_fleet()
        self.logger.debug('end loop')


if __name__ == '__main__':
    test = Test()
    test.TIMEOUT = 0
    test()
