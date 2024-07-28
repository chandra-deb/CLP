# Enums
from enum import Enum


class CharacterStatus(Enum):
    learning = 'learning'
    mastered = 'mastered'
    assumed = 'assumed'
    hard = 'hard'
    hidden = 'hidden'
    blocked = 'blocked'

