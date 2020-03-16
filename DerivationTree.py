from LogicalSignEnum import LogicalSignEnum
import MyException

class DerivationTree:
    """
    Class for building derivation tree from prefixed expression
    Throws MissingOperandDerivationTreeException or MissingOperatorDerivationTreeException if the prefix expression is invalid
    """

    # Constructor
    def __init__(self, prefix_expression):
        """
        string prefix_expression
        NodeTree root
        """

        self.__prefix_expression = prefix_expression
        self.__root = None

        self.__create_derivation_tree()

    # Method
    def __create_derivation_tree(self):
        """
        Create derivation tree

        string prefix_expression
        list<NodeTree> stack
        """

        # Variable
        prefix_expression = self.prefix_expression
        stack = []

        # Remove characters "(" and ")"
        prefix_expression = prefix_expression.replace('(', '')
        prefix_expression = prefix_expression.replace(')', '')

        prefix_expression_array = prefix_expression.split(' ')

        for i in reversed(range(len(prefix_expression_array))):
            x = prefix_expression_array[i]

            # AND operator
            if (x == LogicalSignEnum.AND.value):
                # Operand is missing
                if (len(stack) < 2):
                    raise MyException.MissingOperandDerivationTreeException()

                x_1_node = stack.pop()
                x_2_node = stack.pop()

                node = NodeTree(LogicalSignEnum.AND.name)
                node.left_node = x_1_node
                node.right_node = x_2_node

                stack.append(node)
            # OR operator
            elif (x == LogicalSignEnum.OR.value):
                # Operand is missing
                if (len(stack) < 2):
                    raise MyException.MissingOperandDerivationTreeException()

                x_1_node = stack.pop()
                x_2_node = stack.pop()

                node = NodeTree(LogicalSignEnum.OR.name)
                node.left_node = x_1_node
                node.right_node = x_2_node

                stack.append(node)
            # NOT operator
            elif (x == LogicalSignEnum.NOT.value):
                # Operand is missing
                if (len(stack) < 1):
                    raise MyException.MissingOperandDerivationTreeException()

                x_1_node = stack.pop()

                node = NodeTree(LogicalSignEnum.NOT.name)
                node.left_node = x_1_node

                stack.append(node)
            # Operand
            else:
                node = NodeTree(x)
                stack.append(node)
        
        # Operand is missing
        if (len(stack) != 1):
            raise MyException.MissingOperatorDerivationTreeException()

        self.__root = stack.pop()

    def create_prefix(self):
        """
        Create prefix expression
        """

        return self.__create_prefix(self.root)

    def __create_prefix(self, node):
        # Base case
        if (node.is_leaf()):
            return str(node.value)

        prefix_expression = "(" + node.value + " "

        # Left node
        if (node.has_left_node):
            prefix_expression += self.__create_prefix(node.left_node)
            if (node.has_right_node):
                prefix_expression += " "
        
        # Right node
        if (node.has_right_node):
            prefix_expression += self.__create_prefix(node.right_node)

        prefix_expression += ")"

        return prefix_expression

    def __str__(self):
        return self.create_prefix()

    # Property
    @property
    def root(self):
        """
        root getter
        """

        return self.__root

    @property
    def prefix_expression(self):
        """
        prefix_expression getter
        """

        return self.__prefix_expression

class NodeTree:
    """
    Node representation
    """

    ID = 1

    # Constructor
    def __init__(self, value):
        """
        int id
        string value
        NodeTree left_node
        NodeTree right_node
        boolean has_left_node
        boolean has_right_node
        """

        self.__id = NodeTree.ID
        NodeTree.ID += 1
        self.__value = value
        self.left_node = None
        self.right_node = None

    # Method
    def is_leaf(self):
        """
        Returns true if the node is a leaf (does not have any children)
        """

        return ((self.left_node is None) and (self.right_node is None))

    def __str__(self):
        temp = "Value: " + self.value + ", id: " + str(self.id)

        temp += ", Left node: "
        if (self.has_left_node):
            temp += self.left_node.value
        else:
            temp += "None"

        temp += ", Right node: "
        if (self.has_right_node):
            temp += self.right_node.value
        else:
            temp += "None"

        return temp

    # Property
    @property
    def value(self):
        """
        value getter
        """

        return self.__value

    @property
    def left_node(self):
        """
        left_node getter
        """

        return self.__left_node

    @left_node.setter
    def left_node(self, new_left_node):
        """
        left_node setter
        Changes has_left_node value
        """

        self.__left_node = new_left_node

        if (new_left_node is None):
            self.__has_left_node = False
        else:
            self.__has_left_node = True

    @property
    def right_node(self):
        """
        right_node getter
        """

        return self.__right_node

    @right_node.setter
    def right_node(self, new_right_node):
        """
        right_node setter
        Changes has_right_node value
        """

        self.__right_node = new_right_node

        if (new_right_node is None):
            self.__has_right_node = False
        else:
            self.__has_right_node = True

    @property
    def has_left_node(self):
        """
        has_left_node getter
        """

        return self.__has_left_node

    @property
    def has_right_node(self):
        """
        has_right_node getter
        """

        return self.__has_right_node

    @property
    def id(self):
        """
        id getter
        """

        return self.__id