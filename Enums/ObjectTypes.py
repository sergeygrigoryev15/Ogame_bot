# coding=utf-8
from Core.Enum import Enum


class ObjectTypes(Enum):
    PLANET = 'p'
    MOON = 'm'
    DEBRIS = 'd'

    ALL = [PLANET, MOON, DEBRIS]
