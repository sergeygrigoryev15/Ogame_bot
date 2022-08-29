from enum import Enum


class FleetMissionTypes(Enum):
    ATTACK = '1'
    TRANSPORT = '3'
    LEAVE = '4'
    ESPIONAGE = '6'
    EXPEDITION = '15'
    COLONIZATION = '7'
    RECYCLE = '8'
    LOOK_FOR_LIFE = '18'
