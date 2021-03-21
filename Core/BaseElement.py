from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from Core.BaseEntity import BaseEntity


class BaseElement(BaseEntity):

    def __init__(self, identifier, id_type=By.XPATH):
        BaseEntity.__init__(self)
        self.identifier = identifier
        self.id_type = id_type
        self.web_element = None

    @property
    def element(self):
        if self.web_element:
            return self.web_element
        self.web_element = self.driver.find_element(self.id_type, self.identifier)
        return self.web_element

    @property
    def x_path(self):
        if self.id_type is By.XPATH:
            return self.identifier
        return f'//*[@{self.id_type}="{self.identifier}"]'

    def hover_mouse(self):
        action = ActionChains(self.driver).move_to_element(self.element)
        action.perform()
