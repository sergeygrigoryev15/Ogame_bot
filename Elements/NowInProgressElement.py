from Elements.WebElement import WebElement
from Enums.QueueTypes import QueueTypes


class NowInProgressElement(object):

    def __init__(self, queue_types: QueueTypes = QueueTypes):
        self.queue_types = queue_types
        self.__elements = {}
        self.__init()

    def __init(self):
        for el in self.queue_types:
            self.__elements[el] = QueueElement(el)

    def __getitem__(self, item):
        if item in self.__elements:
            return self.__elements.get(item)()


class QueueElement(WebElement):

    def __init__(self, queue_type):
        self.base_xpath = '//*[@class="content-box-s"]'
        self.xpath = self.base_xpath + f'[./*[@class="header" and contains(., "{queue_type}")]]'
        WebElement.__init__(self, self.xpath)

    def __call__(self):
        data = {}
        name = self.name
        if not name:
            return
        data.update({'name': name, 'level': self.level, 'time': self.time})
        return data

    @property
    def name(self):
        name = self.find_element_by_xpath('//*[@colspan="2"]')
        cls = name.get_attribute('class')
        if cls and cls == 'idle':
            return
        return name.get_text()

    @property
    def level(self):
        level = self.find_element_by_xpath('//*[@class="level"]')
        return level.get_text()

    @property
    def time(self):
        time = self.find_element_by_xpath('//*[@id="Countdown"]')
        return time.get_text()
