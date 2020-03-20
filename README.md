# SATSolver

## formula2cnf.py ##
Program which translates a description of a formula in NNF into a DIMACS CNF formula using Tseitin encoding.\n
formula2cnf.py [-one_sided] [input_path [output_path]]

## dpllTask.py ##
DPLL solver which implements the basic branch and bound DPLL algorithm with unit propagation.\n
dpllTask.py [-DIMACS | -SMT-LIB] input_path