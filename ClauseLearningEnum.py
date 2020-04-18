from enum import Enum

class ClauseLearningEnum(Enum):
    none = 0
    StopAtTheFirstUIP = 1
    StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent = 2