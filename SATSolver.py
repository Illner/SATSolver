from DerivationTree import DerivationTree
from LogicalSignEnum import LogicalSignEnum
from TseitinEncoding import TseitinEncoding
from DPLL import DPLL
from CNF import CNF
import MyException

text = "(or a1 (and a2 (and a3 (and a4 a5))))"

derivationTree = DerivationTree(text)
tseitinEncoding = TseitinEncoding(derivationTree, False)
DIMACS_format = str(tseitinEncoding)
print(DIMACS_format)

cnf = CNF(DIMACS_format, tseitinEncoding.original_variable_dictionary)
print("number_of_clauses: " + str(cnf.number_of_clauses))
print("number_of_variables: " + str(cnf.number_of_variables))
print(cnf.cnf)

dpll = DPLL(cnf)
result = dpll.DPLL()

print(str(dpll.number_of_decisions))
print(str(dpll.number_of_steps_of_unit_propagation))

print(result)