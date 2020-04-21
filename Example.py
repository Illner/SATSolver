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
          clause_deletion_how_heuristic_enum=ClauseDeletionHowHeuristicEnum.KeepActiveClauses,
          bound_keep_short_clauses_heuristic = 2,
          ratio_keep_active_clauses_heuristic = 0.5)
cnf.add_learned_clause([1])
cnf.add_learned_clause([1, -2])
cnf.add_learned_clause([2, 3])
cnf.add_learned_clause([2, -4, 5])
cnf.add_learned_clause([-5])


nevim = set()
nevim.add(4)
cnf.set_active_learned_clause_hashset(nevim)

nevim = {}
nevim[1] = 1
nevim[2] = 2
cnf.set_active_counter_learned_clause_dictionary(nevim)

print("--------------------------------------------------------------------------------------------------")
print("Learned clauses: {0}".format(cnf.learned_clauses))
print("Number of learned clauses: {0}".format(cnf.number_of_learned_clauses))
print("antecedent_dictionary: {0}".format(cnf.antecedent_dictionary))
print("active_learned_clause_hashset: {0}".format(cnf.active_learned_clause_hashset))

if (keep_active):
    print("\nKeep active")
    print("active_counter_learned_clause_dictionary: {0}".format(cnf.active_counter_learned_clause_dictionary))

if (adjacency_list):
    print("\nAdjacency list")
    print("counter_learned_clause_list: {0}".format(cnf.counter_learned_clause_list))
    print("adjacency_list_learned_clause_dictionary: {0}".format(cnf.adjacency_list_learned_clause_dictionary))
    print("unit_learned_clause_list: {0}".format(cnf.unit_learned_clause_list))
    print("contradiction_learned_clause_list: {0}".format(cnf.contradiction_learned_clause_list))

if (not adjacency_list):
    print("\nWatched literals")
    print("learned_clause_watched_literals_list: {0}".format(cnf.learned_clause_watched_literals_list))
    print("variable_watched_literals_learned_clause_dictionary: {0}".format(cnf.variable_watched_literals_learned_clause_dictionary))

print()
print("--------------------------------------------------------------------------------------------------")
print("--------------------------------------------------------------------------------------------------")

cnf.clause_deletion()

print("Learned clauses: {0}".format(cnf.learned_clauses))
print("Number of learned clauses: {0}".format(cnf.number_of_learned_clauses))
print("antecedent_dictionary: {0}".format(cnf.antecedent_dictionary))
print("active_learned_clause_hashset: {0}".format(cnf.active_learned_clause_hashset))

if (keep_active):
    print("\nKeep active")
    print("active_counter_learned_clause_dictionary: {0}".format(cnf.active_counter_learned_clause_dictionary))

if (adjacency_list):
    print("\nAdjacency list")
    print("counter_learned_clause_list: {0}".format(cnf.counter_learned_clause_list))
    print("adjacency_list_learned_clause_dictionary: {0}".format(cnf.adjacency_list_learned_clause_dictionary))
    print("unit_learned_clause_list: {0}".format(cnf.unit_learned_clause_list))
    print("contradiction_learned_clause_list: {0}".format(cnf.contradiction_learned_clause_list))

if (not adjacency_list):
    print("\nWatched literals")
    print("learned_clause_watched_literals_list: {0}".format(cnf.learned_clause_watched_literals_list))
    print("variable_watched_literals_learned_clause_dictionary: {0}".format(cnf.variable_watched_literals_learned_clause_dictionary))
print("--------------------------------------------------------------------------------------------------")