from typing import Union, Optional

from dataclasses import dataclass
from selenium.webdriver.common.by import By

from Elements.WebElement import WebElement
from Screens.BaseOgameScreen import BaseOgameScreen


@dataclass
class PlanetOwner:
    name: str
    on_vocations: bool = False
    noob: bool = False
    admin: bool = False
    ally: bool = False


@dataclass
class Planet:
    position: Union[list, tuple]
    name: str
    owner: Optional[PlanetOwner] = None
    has_moon: bool = False
    has_debris: bool = False


class GalaxyScreen(BaseOgameScreen):
    def __init__(self):
        super().__init__('//*[@id="galaxycomponent"]')

        self.txb_galaxy = WebElement('galaxy_input', id_type=By.ID)
        self.txb_solar_system = WebElement('system_input', id_type=By.ID)
        self.btn_go = WebElement('btn_blue', id_type=By.CLASS_NAME)
        self.planet_container = WebElement('//*[contains(@class, "galaxyRow") and contains(@class, "ContentRow")]')

    @property
    def current_system(self):
        return self.txb_galaxy.get_attribute('value'), self.txb_solar_system.get_attribute('value')

    def select_system(self, galaxy: Optional[str] = None, solar_system: Optional[str] = None):
        current_galaxy, current_solar = self.current_system
        if galaxy and galaxy != current_galaxy:
            self.txb_galaxy.send_keys(galaxy)
        if solar_system and solar_system != current_solar:
            self.txb_solar_system.send_keys(solar_system)
        self.btn_go.click()

    def parse_solar_system(self, galaxy: Optional[str] = None, solar_system: Optional[str] = None):
        self.select_system(galaxy, solar_system)
        current_galaxy, current_solar = self.current_system
        planets = []
        for container in self.planet_container.elements:
            if 'empty' in container.get_attribute('class'):
                continue
            position = container.find_element_by_xpath('.//*[contains(@class, "Position")]').get_text()
            name = container.find_element_by_xpath('.//*[contains(@class, "PlanetName")]').get_text()
            has_debris = 'galaxy_debris' in \
                         container.find_element_by_xpath('.//*[contains(@class, "cellDebris")]').get_attribute('class')
            has_moon = WebElement(
                container.x_path + './/*[contains(@class, "cellMoon")]//*[@data-moon-id]').is_present()
            owner_container = container.find_element_by_xpath('.//*[contains(@class, "PlayerName")]')
            owner_container.hover_mouse()
            # TODO refactor this to custom elements and fix exceptions
            try:
                owner_container = owner_container.find_element_by_xpath('.//*[contains(@rel, "player")]')
                owner_class = owner_container.get_attribute('class')
                owner_name = owner_container.get_text()
                is_admin = 'admin' in owner_class
                is_vacation = 'vacation' in owner_class
                is_noob = 'noob' in owner_class
            except Exception:
                owner_name = 'Undefined'
                is_admin = False
                is_vacation = False
                is_noob = False
            finally:
                self.btn_go.hover_mouse()
                self.sleep(1)
            alliance_container = container.find_element_by_xpath('.//*[contains(@class, "Alliance")]')
            alliance_container.hover_mouse()
            try:
                alliance = WebElement(alliance_container.x_path + './/*[contains(@rel, "alliance")]')
                is_ally = alliance.is_present() and 'ally' in alliance.get_attribute('class')
            except Exception:
                is_ally = False

            planets.append(
                Planet(
                    position=[current_galaxy, current_solar, position],
                    name=name,
                    owner=PlanetOwner(owner_name, on_vocations=is_vacation, noob=is_noob, admin=is_admin, ally=is_ally),
                    has_moon=has_moon,
                    has_debris=has_debris
                )
            )
        return planets

    def get_planets(self):
        return self.parse_solar_system()
