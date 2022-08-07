from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Core.BaseEntity import BaseEntity


WAIT_ELEMENT_PRESENT_TIMEOUT = 10


class BaseElement(BaseEntity):
    def __init__(self, identifier: str, id_type: 'By' = By.XPATH):
        BaseEntity.__init__(self)
        self.identifier = identifier
        self.id_type = id_type
        self.web_element = None

    @property
    def element(self):
        if not self.web_element:
            self.web_element = WebDriverWait(
                self.driver, WAIT_ELEMENT_PRESENT_TIMEOUT
            ).until(EC.presence_of_element_located((self.id_type, self.identifier)))
        return self.web_element

    @property
    def x_path(self) -> str:
        if self.id_type is By.XPATH:
            return self.identifier
        return f'//*[@{self.id_type}="{self.identifier}"]'

    def hover_mouse(self) -> None:
        action = ActionChains(self.driver).move_to_element(self.element)
        action.perform()
