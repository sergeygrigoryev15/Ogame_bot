# coding=utf-8
from Core.Enum import Enum


class QueueTypes(Enum):
    BUILDINGS = 'Постройки'
    RESEARCHES = 'Исследования'
    DOCK = 'Верфь'

    ALL = [BUILDINGS, RESEARCHES, DOCK]
