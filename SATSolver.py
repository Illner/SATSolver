from DerivationTree import DerivationTree
from LogicalSignEnum import LogicalSignEnum
from TseitinEncoding import TseitinEncoding
import MyException

text = "(or a1 (and a2 (and a3 (and a4 a5))))"

derivationTree = DerivationTree(text)
# print(derivationTree)
tseitinEncoding = TseitinEncoding(derivationTree, True)
print(tseitinEncoding)

# try:
#     derivationTree = DerivationTree(text)
#     print(derivationTree)
#     print(derivationTree.prefix_expression)
# except MyException.MissingOperandDerivationTreeException as e:
#     print(e)
# except MyException.MissingOperatorDerivationTreeException as e:
#     print(e)