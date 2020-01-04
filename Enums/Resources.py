from Core.Enum import Enum


class Resources(Enum):
    METAL = 'metal'
    CRYSTAL = 'crystal'
    DEUTERIUM = 'deuterium'
    DARK_MATTER = 'darkmatter'
    ENERGY = 'energy'

    ALL = [METAL, CRYSTAL, DEUTERIUM, DARK_MATTER, ENERGY]
