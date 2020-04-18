from CNF import CNF
from CDCL import CDCL
from ClauseLearningEnum import ClauseLearningEnum
from UnitPropagationEnum import UnitPropagationEnum
from ClauseDeletionHeuristicEnum import ClauseDeletionHowHeuristicEnum
from ClauseDeletionHeuristicEnum import ClauseDeletionWhenHeuristicEnum

temp =  """c
c start with comments
c
c 
p cnf 3 2
1 0
1 2 3 0"""

cnf = CNF(temp, unit_propagation_enum=UnitPropagationEnum.WatchedLiterals, clause_learning_enum = ClauseLearningEnum.StopAtTheFirstUIP, clause_deletion_how_heuristic_enum=ClauseDeletionHowHeuristicEnum.none)
cnf.add_literal_to_partial_assignment(-3)
cnf.add_learned_clause([2, 3])
cnf.unit_propagation()
cnf.add_learned_clause([2])

print("CNF: ")
print(cnf.cnf)

print("Learned clauses: ")
print(cnf.learned_clauses)

print("Partial assignment: ")
print(cnf.partial_assignment_with_levels)

# print("Dictionary: ")
# print(cnf.variable_watched_literals_learned_clause_dictionary)

# print("Watched literals list: ")
# print(cnf.learned_clause_watched_literals_list)

print("Active_counter_learned_clause_dictionary: ")
print(cnf.active_counter_learned_clause_dictionary)

print("Antecedent_dictionary: ")
print(cnf.antecedent_dictionary)

print("active_learned_clause_hashset: ")
print(cnf.active_learned_clause_hashset)
