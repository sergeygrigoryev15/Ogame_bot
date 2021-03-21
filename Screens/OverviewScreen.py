from Elements.NowInProgressElement import NowInProgressElement
from Screens.BaseOgameScreen import BaseOgameScreen


class OverviewScreen(BaseOgameScreen):
    def __init__(self):
        BaseOgameScreen.__init__(self, '//*[@id="planet"]')
        self.queue = NowInProgressElement()
