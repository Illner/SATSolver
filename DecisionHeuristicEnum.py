from enum import Enum

class DecisionHeuristicEnum(Enum):
    Greedy = 0,
    Random = 1,
    JeroslowWangOneSided = 2,
    JeroslowWangTwoSided = 3,
    JeroslowWangOneSidedDynamic = 4,
    JeroslowWangTwoSidedDynamic = 5,
    VSIDS = 6,
    eVSIDS = 7