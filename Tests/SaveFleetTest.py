from datetime import timedelta

from Bot.SlackChannels import SlackChannels
from Commands.Commands import commands
from Core.BaseInfiniteTest import BaseInfiniteTest
from Enums.FleetMissionTypes import FleetMissionTypes
from Screens.OverviewScreen import OverviewScreen


class SaveFleetTest(BaseInfiniteTest):

    SAVE_FLEET_TIMEOUT = timedelta(minutes=10)

    def main_loop(self):
        self.logger.add('start loop')
        overview_screen = OverviewScreen()
        log = overview_screen.fleetAlertsTab.get_log()
        if log:
            self.logger.add('log = ')
            self.logger.add(self.logger.make_table([el.__str__() for el in log], coloring={'is_friendly': lambda x: x}))
        enemy_fleets = \
            filter(
                lambda el:
                el.is_friendly is False and
                el.mission_type == FleetMissionTypes.ATTACK and
                not el.is_return, log)
        for fleet in enemy_fleets:
            if fleet.remaining_time < self.SAVE_FLEET_TIMEOUT:
                self.slack_bot.send_message(
                    'we are under attack:\n{} ({})'.format(fleet.to_coordinates, fleet.remaining_time),
                    channel=SlackChannels.ALERTS)
                commands.save_fleet(fleet.to_coordinates)
        commands.return_fleet()
        self.logger.add('end loop')


if __name__ == '__main__':
    test = SaveFleetTest()
    test()
