from DerivationTree import DerivationTree
import MyException

text = "(and (or (and (or (and (or (and x1 (not x4)) (and x3 x9)) (or (and x7 x1) (and x4 x9))) (and (or (and x9 x9) (and (not x4) (not x5))) (or (and x3 (not x6)) (and (not x3) x6)))) (or (and (or (and x2 (not x2)) (and (not x6) (not x1))) (or (and (not x9) x7) (and x9 (not x6)))) (and (or (and x2 x4) (and (not x2) x2)) (or (and (not x5) (not x6)) (and x6 (not x4)))))) (and (or (and (or (and (not x2) x9) (and x3 (not x7))) (or (and (not x9) x6) (and x4 x6))) (and (or (and (not x5) x4) (and (not x4) (not x7))) (or (and (not x3) (not x3)) (and x9 (not x7))))) (or (and (or (and (not x6) x3) (and (not x2) x2)) (or (and x3 (not x2)) (and (not x7) (not x9)))) (and (or (and (not x9) x2) (and (not x6) x5)) (or (and (not x3) (not x1)) (and (not x9) x9)))))) (or (and (or (and (or (and x5 x3) (and (not x3) x6)) (or (and (not x1) x6) (and (not x4) x4))) (and (or (and x2 (not x2)) (and x3 (not x9))) (or (and x5 (not x4)) (and x5 (not x6))))) (or (and (or (and (not x9) (not x2)) (and x4 x6)) (or (and x9 x4) (and x2 x4))) (and (or (and x1 (not x2)) (and x5 (not x4))) (or (and x8 x8) (and (not x4) x2))))) (and (or (and (or (and (not x6) (not x7)) (and (not x1) x1)) (or (and (not x6) x4) (and x4 (not x3)))) (and (or (and (not x3) (not x8)) (and x2 (not x9))) (or (and x1 x2) (and x3 (not x8))))) (or (and (or (and (not x4) (not x1)) (and x7 x7)) (or (and (not x8) (not x7)) (and (not x3) x5))) (and (or (and x1 x6) (and x1 (not x9))) (or (and x1 x3) (and x2 x7)))))))"

try:
    derivationTree = DerivationTree(text)
    print(derivationTree)
    print(derivationTree.prefix_expression)
except MyException.MissingOperandDerivationTreeException as e:
    print(e)
except MyException.MissingOperatorDerivationTreeException as e:
    print(e)