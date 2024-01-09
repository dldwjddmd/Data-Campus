from enum import Enum, unique
from operator import ge, gt, le, lt, eq

@unique
class ObjectCategory(Enum):
    """
    Bicycle
    Kickboard
    Motorcycle
    """
    BICYCLE = 'bicycle'
    KICKBOARD = 'kickboard'
    MOTORCYCLE = 'motorcycle'

    def __int__(self):
        if self == ObjectCategory.MOTORCYCLE:
            return 0
        elif self == ObjectCategory.BICYCLE:
            return 1
        elif self == ObjectCategory.KICKBOARD:
            return 2
        else:
            return -1


@unique
class RiskCategory(Enum):
    """
    Low  = 0
    Mid  = 1
    High = 2
    """
    LOW = 0
    MID = 1
    HIGH = 2

    def __eq__(self, other):
        if type(other) == RiskCategory:
            return eq(self.value, other.value)
        else:
            return False
    
    def __gt__(self, other):
        if type(other) == RiskCategory:
            return gt(self.value, other.value)
        else:
            return False

    def __ge__(self, other):
        if type(other) == RiskCategory:
            return ge(self.value, other.value)
        else:
            return False

    def __lt__(self, other):
        if type(other) == RiskCategory:
            return lt(self.value, other.value)
        else:
            return False

    def __le__(self, other):
        if type(other) == RiskCategory:
            return le(self.value, other.value)
        else:
            return False



