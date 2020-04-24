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
p cnf 5 2
1 0
1 2 3 0"""

keep_active = True
adjacency_list = True

cnf = CNF(temp, 
          unit_propagation_enum=UnitPropagationEnum.AdjacencyList, 
          clause_learning_enum = ClauseLearningEnum.StopAtTheFirstUIP, 
          clause_deletion_how_heuristic_enum=ClauseDeletionHowHeuristicEnum.RemoveSubsumedClauses,
          bound_keep_short_clauses_heuristic = 2,
          ratio_keep_active_clauses_heuristic = 0.5)
cnf.add_learned_clause([1])
cnf.add_learned_clause([2, 3])
cnf.add_learned_clause([2, -4, -5])


nevim = set()
cnf.set_active_learned_clause_hashset(nevim)

print("--------------------------------------------------------------------------------------------------")
print("Learned clauses: {0}".format(cnf.learned_clauses))
print("Number of learned clauses: {0}".format(cnf.number_of_learned_clauses))
print("active_learned_clause_hashset: {0}".format(cnf.active_learned_clause_hashset))

print()
print("--------------------------------------------------------------------------------------------------")
print("--------------------------------------------------------------------------------------------------")

cnf.clause_deletion()

print("Learned clauses: {0}".format(cnf.learned_clauses))
print("Number of learned clauses: {0}".format(cnf.number_of_learned_clauses))
print("active_learned_clause_hashset: {0}".format(cnf.active_learned_clause_hashset))