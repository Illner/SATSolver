from enum import Enum

class ClauseDeletionHowHeuristicEnum(Enum):
    none = 0,
    RemoveSubsumedClauses = 1,
    KeepShortClauses = 2,
    KeepShortClausesAndRemoveSubsumedClauses = 3,
    KeepActiveClauses = 4,
    KeepActiveClausesAndRemoveSubsumedClauses = 5

class ClauseDeletionWhenHeuristicEnum(Enum):
    none = 0,
    Restart = 1,
    CacheFull = 2