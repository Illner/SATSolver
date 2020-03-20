from DerivationTree import DerivationTree
from LogicalSignEnum import LogicalSignEnum
from TseitinEncoding import TseitinEncoding
from Cnf import Cnf
import MyException

text = "(or a1 (and a2 (and a3 (and a4 a5))))"

derivationTree = DerivationTree(text)
tseitinEncoding = TseitinEncoding(derivationTree, False)
DIMACS_format = str(tseitinEncoding)
print(DIMACS_format)
cnf = Cnf(DIMACS_format, tseitinEncoding.original_variable_dictionary)
print("number_of_clauses: " + str(cnf.number_of_clauses))
print("number_of_variables: " + str(cnf.number_of_variables))
print(cnf.cnf)