import time

from Elements.WebElement import WebElement


class PlanetsList(WebElement):
    def __init__(self):
        self.xpath = '//div[@id="planetList"]'
        WebElement.__init__(self, self.xpath)

        self.planet_template = self.xpath + '//a[contains(@class, "planetlink")]'
        self.planet_name = './*[contains(@class, "planet-name")]'
        self.planet_koords = './*[contains(@class, "planet-koords")]'
        self.selected_planet = (
            self.planet_template
            + '[contains(@class, "active")]'
            + self.planet_koords[1:]
        )

    @property
    def data(self):
        data = {}
        for element in WebElement(self.planet_template).elements:
            name = element.find_element_by_xpath(self.planet_name).get_text()
            coordinate = element.find_element_by_xpath(self.planet_koords).get_text()
            data[coordinate] = name
        return data

    @property
    def active_planet(self):
        if len(self.data) == 1:
            return self.data.popitem()
        return WebElement(self.selected_planet).get_text()

    def select_planet(self, planet):
        if self.active_planet != planet:
            for _ in range(5):
                WebElement(
                    self.xpath
                    + f'/*[contains(@id, "planet-")][./*[contains(.,"{planet}")]]'
                ).click()
                time.sleep(2)
                if self.active_planet == planet:
                    break
