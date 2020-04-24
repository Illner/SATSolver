import os
import random
import matplotlib.pyplot as plt

from CNF import CNF
from CDCL import CDCL
from ClauseLearningEnum import ClauseLearningEnum
from UnitPropagationEnum import UnitPropagationEnum
from ClauseDeletionHeuristicEnum import ClauseDeletionHowHeuristicEnum
from ClauseDeletionHeuristicEnum import ClauseDeletionWhenHeuristicEnum

# Variable
x_axis_variables = [20, 50, 75, 100]

y_1 = [0.0361328125, 4.05859375, 93.4140625, 260.15625]
y_2 = [0.0234375, 3.546875, 46.5625, 151.015625]
y_3 = [0.04296875, 3.28125, 56.1640625, 111.359375]
y_4 = [0.0361328125, 4.04296875, 78.421875, 164.9375]
y_5 = [0.0302734375, 3.49609375, 75.40625, 182.453125]

# Number of clause deletions
plt.plot(x_axis_variables, y_1, color="blue", label='RemoveSubsumedClauses')
plt.plot(x_axis_variables, y_2, color="red", label='KeepShortClauses')
plt.plot(x_axis_variables, y_3, color="purple", label='KeepShortClausesAndRemoveSubsumedClauses')
plt.plot(x_axis_variables, y_4, color="green", label='KeepActiveClauses')
plt.plot(x_axis_variables, y_5, color="yellow", label='KeepActiveClausesAndRemoveSubsumedClauses')
plt.title('Number of deleted learned clauses')
plt.xlabel('Number of variables')
plt.ylabel('Number of deleted learned clauses')
plt.legend(loc="upper left")
plt.show()