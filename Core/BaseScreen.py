import time

from Core.BaseEntity import BaseEntity
from Elements.WebElement import WebElement

TIMEOUT = 60


class BaseScreen(BaseEntity):
    def __init__(self, xpath: str):
        BaseEntity.__init__(self)
        self.xpath = xpath
        self.wait_for_page_to_load()

    def wait_for_page_to_load(self, timeout: int = TIMEOUT) -> None:
        start_time = time.time()
        while time.time() < start_time + timeout:
            try:
                if WebElement(self.xpath).is_present():
                    return
            except Exception:
                continue
        else:
            raise AssertionError(
                f'Screen {self.__class__.__name__} was not opened in {timeout} seconds'
            )
