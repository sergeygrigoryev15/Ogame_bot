from Elements.WebElement import WebElement
from Enums.MenuTabs import MenuTabs


class NavigationMenu(WebElement):

    def __init__(self):
        self.xpath = '//*[@id="menuTable"]'
        WebElement.__init__(self, self.xpath)

        self.menu_item_template = self.xpath + '//a[contains(@class, "menubutton")]/*[contains(., "{}")]'
        self.active_menu_item = self.xpath + '//a[contains(@class, "menubutton") and contains(@class, "selected")]/*[@class="textlabel"]'

        self.fleet_movements_tab_path = '//*[contains(@class, "fleet1")]'

    def open_tab(self, tab):
        if tab == MenuTabs.FLEET_MOVEMENTS:
            element = WebElement(self.fleet_movements_tab_path)
        else:
            element = WebElement(self.menu_item_template.format(tab))
        element.click()

    @property
    def active_tab(self):
        element = WebElement(self.active_menu_item)
        return MenuTabs.get_by_name(element.get_text())
