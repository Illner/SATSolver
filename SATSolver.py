from DerivationTree import DerivationTree
from LogicalSignEnum import LogicalSignEnum
from TseitinEncoding import TseitinEncoding
import MyException

text = "(or a1 (and a2 (and a3 (and a4 a5))))"

derivationTree = DerivationTree(text)
# print(derivationTree)
tseitinEncoding = TseitinEncoding(derivationTree, False)
print(tseitinEncoding)

print("----")
nevim = tseitinEncoding.original_variable_dictionary
for i in nevim:
    print(str(i) + ": " + nevim[i])

# try:
#     derivationTree = DerivationTree(text)
#     print(derivationTree)
#     print(derivationTree.prefix_expression)
# except MyException.MissingOperandDerivationTreeException as e:
#     print(e)
# except MyException.MissingOperatorDerivationTreeException as e:
#     print(e)