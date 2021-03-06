# SATSolver

## formula2cnf.py ##
Program which translates a description of a formula in NNF into a DIMACS CNF formula using Tseitin encoding.

formula2cnf.py [-one_sided] [input_path [output_path]]

## dpllAlgorithm.py ##
DPLL solver which implements the basic branch and bound DPLL algorithm with unit propagation.

dpllAlgorithm.py [-DIMACS | -SMT-LIB] input_path

## cdclAlgorithm.py ##
CDCL solver

cdclAlgorithm.py [-ClauseLearning=X] [-RestartStrategy=X] [-ClauseDeletionWhenHeuristic=X] [-ClauseDeletionHowHeuristic=X] [-DecisionHeuristic=X] [-WatchedLiterals | -AdjacencyList] [-DIMACS | -SMT-LIB] [-Assumptions=[literal_1, literal_2, ...]] input_path 

### ClauseLearning ###
1 - stop at the first UIP (**DEFAULT**)

2 - stop when the literal at current decision level has no antecedent

### RestartStrategy ###
How to determine when the search should be restarted:

1 - Luby strategy (**DEFAULT**)

2 - geometric strategy

### ClauseDeletionWhenHeuristic ###
How to determine when the learned clauses should be deleted:

1 - at the time of restart (**DEFAULT**)

2 - when the current cache is full

### ClauseDeletionHowHeuristic ###
A heuristic for regularly deleting some of the learned clauses:

1 - remove subsumed clauses

2 - keep short clauses

3 - keep short clauses and remove subsumed clauses

4 - keep active clauses (**DEFAULT**)

5 - keep active clauses and remove subsumed clauses

6 - keep active clauses (version 2)

7 - keep active clauses (version 2) and remove subsumed clauses

### DecisionHeuristic ###
1 - first literal, which is found, is used

2 - literal is picked randomly (all pickable literals have same weights)

3 - Jeroslow-Wang one-sided

4 - Jeroslow-Wang one-sided dynamic

5 - Jeroslow-Wang two-sided

6 - Jeroslow-Wang two-sided dynamic

7 - VSIDS

8 - eVSIDS (**DEFAULT**)

# Applications

## nQueensProblem.py ##
Model the N-queens problem as a SAT problem.

nQueensProblem.py size_of_board [output_path]