from loguru import logger

from Elements.WebElement import WebElement
from Enums.Resources import Resources


class ResourcesTab(WebElement):
    def __init__(self):
        self.xpath = '//*[@id="resources"]'
        WebElement.__init__(self, self.xpath)
        self.resources_data = {}
        self.resource_container_template = self.xpath + '/li[@id="{resource_type}_box"]'
        self.resource_value_template = (
            self.resource_container_template
            + '//*[@class="value"]/*[@id="resources_{resource_type}"]'
        )
        self.tooltip_template = '//*[contains(@class, "tooltip")][.//*[contains(@style, "visible")]]//*[@class="htmlTooltip"]//table'
        self.element_in_tooltip_template = (
            '(' + self.tooltip_template + '//td)[{}]/span'
        )

    def get_current_count(self, resource_type: Resources):
        element = WebElement(
            self.resource_value_template.format(resource_type=resource_type.value)
        )
        value = element.get_int()
        return value

    def __open_tooltip(self, resource_type: Resources):
        element = WebElement(
            self.resource_value_template.format(resource_type=resource_type.value)
        )
        element.hover_mouse()

    def get_main_resource_info(self, resource: Resources):
        data = {}
        self.__open_tooltip(resource)
        storage_capacity = WebElement(self.element_in_tooltip_template.format(2))
        dig_velocity = WebElement(self.element_in_tooltip_template.format(3))
        safe_storage_capacity = WebElement(self.element_in_tooltip_template.format(4))
        data.update(
            {
                'dig_velocity': int(dig_velocity.get_int()),
                'storage_capacity': int(storage_capacity.get_int()),
                'safe_storage_capacity': int(safe_storage_capacity.get_int()),
            }
        )
        return data

    def get_dark_matter_info(self):
        data = {}
        self.__open_tooltip(Resources.DARK_MATTER)
        bought = WebElement(self.element_in_tooltip_template.format(2))
        found = WebElement(self.element_in_tooltip_template.format(3))
        data.update({'bought': int(bought.get_int()), 'found': int(found.get_int())})
        return data

    def get_energy_info(self):
        data = {}
        self.__open_tooltip(Resources.ENERGY)
        produced = WebElement(self.element_in_tooltip_template.format(2))
        used = WebElement(self.element_in_tooltip_template.format(3))
        data.update({'produced': int(produced.get_int()), 'used': int(used.get_int())})
        return data

    def init_data(self):
        for r in Resources:
            tmp_data = {}
            tmp_data.update({'available': self.get_current_count(r)})
            if r in [Resources.METAL, Resources.CRYSTAL, Resources.DEUTERIUM]:
                tmp_data.update(**self.get_main_resource_info(r))
            elif r == Resources.DARK_MATTER:
                tmp_data.update(**self.get_dark_matter_info())
            elif r == Resources.ENERGY:
                tmp_data.update(**self.get_energy_info())
            else:
                logger.warning(f'Unsupported resource type "{r}"')
            self.resources_data.update({r: tmp_data})

    @property
    def data(self):
        if not self.resources_data:
            self.init_data()
        return self.resources_data
