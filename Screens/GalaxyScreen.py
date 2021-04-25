from typing import Union

from dataclasses import dataclass
from selenium.webdriver.common.by import By

from Elements.WebElement import WebElement
from Screens.BaseOgameScreen import BaseOgameScreen


@dataclass
class PlanetOwner:
    name: str
    on_vocations: bool
    noob: bool
    admin: bool


@dataclass
class Planet:
    position: Union[list, tuple]
    name: str
    has_moon: bool
    has_debris: bool
    owner: PlanetOwner


class GalaxyScreen(BaseOgameScreen):
    def __init__(self):
        super().__init__('//*[@id="galaxycomponent"]')

        self.txb_galaxy = WebElement('galaxy_input', id_type=By.ID)
        self.txb_solar_system = WebElement('system_input', id_type=By.ID)
        self.btn_go = WebElement('btn_blue', id_type=By.CLASS_NAME)

    def get_planets(self):
        # TODO make this work properly
        return [
            Planet(
                [1, 29, 4],
                'Planet1',
                False,
                False,
                PlanetOwner('Homeless', False, False, False),
            )
        ]
