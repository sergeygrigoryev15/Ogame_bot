# coding=utf-8
import re
from datetime import datetime

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from Core.BaseElement import BaseElement


class WebElement(BaseElement):

    def __init__(self, identifier=None, id_type=By.XPATH, element=None):
        BaseElement.__init__(self, identifier, id_type)
        if element:
            self.__setattr__('web_element', element)

    def click(self):
        try:
            self.element.click()
        except Exception:
            self.click_via_js()

    def click_via_js(self):
        self.driver.execute_script('arguments[0].click();', self.element)

    def send_keys(self, text):
        self.element.send_keys(text)

    def get_text(self):
        return self.element.text

    def get_int(self):
        text = self.element.text
        to_replace = ['.', ',', '+', '-']
        for el in to_replace:
            text = text.replace(el, '')
        return int(text)

    def get_time(self):
        text = self.element.text
        to_replace = [u'д', u'ч', u'м', u'с']
        for el in to_replace:
            text = text.replace(el, '')
        text = text.strip()
        text = text.replace(':', ' ')
        time = datetime.strptime(text, '%d %H %M %S')
        return time

    def get_coordinates(self):
        text = self.element.text
        coordRegex = r'^[(/d+):(/d+):(/d+)]$'
        search = re.search(coordRegex, text)
        if search:
            return search.group(1), search.group(2), search.group(3)

    def is_present(self):
        try:
            elem = self.element
        except NoSuchElementException:
            return False
        return elem.is_displayed()

    def get_attribute(self, attr):
        return self.element.get_attribute(attr)

    def find_element_by_xpath(self, xpath):
        element = self.element.find_element_by_xpath(xpath)
        return WebElement(element=element)

    @property
    def elements(self):
        return [WebElement(identifier=self.identifier, id_type=self.id_type, element=el) for el in
                self.driver.find_elements(self.id_type, self.identifier)]
