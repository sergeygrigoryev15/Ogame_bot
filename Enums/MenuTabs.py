# coding=utf-8
from Core.Enum import Enum


class MenuTabs(Enum):
    OVERVIEW = 'Обзор'
    RESOURCES = 'Сырьё'
    FABRIKS = 'Фабрики'
    RESEARCH = 'Исследования'
    DOCK = 'Верфь'
    DEFENCE = 'Оборона'
    FLEET = 'Флот'
    GALAXY = 'Галактика'
    ALIANCE = 'Альянс'
    FLEET_MOVEMENTS = 'Fleet Movements'

    ALL = [OVERVIEW, RESOURCES, FABRIKS, RESEARCH, DOCK, DEFENCE, FLEET, GALAXY, ALIANCE]
