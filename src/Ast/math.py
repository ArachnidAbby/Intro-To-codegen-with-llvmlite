import errors
from Ast.basenodes import ExpressionNode


class Operation(ExpressionNode):
    __slots__ = ("lhs", "rhs", "op", "parent")

    needs_parent = True

    def __init__(self, pos, op: str, lhs, rhs):
        super().__init__(pos)

        self.lhs = lhs
        self.rhs = rhs
        self.op = op
        self.parent = None

    def pre_eval(self, func):
        if self.lhs.needs_parent:
            self.lhs.parent = self.parent
        if self.rhs.needs_parent:
            self.rhs.parent = self.parent

        self.lhs.pre_eval(func)
        self.rhs.pre_eval(func)

        lhs_typ = self.lhs.ret_type

        if lhs_typ is None:
            errors.error("An error occured. left hand side of " +
                         "operation did not return",
                         loc=self.lhs.position)
            return

        self.ret_type = lhs_typ.get_op_return(func,
                                              self.op,
                                              self.lhs,
                                              self.rhs)

    def eval(self, func):
        global operations
        op_func = operations[self.op]
        return op_func(func, self.lhs, self.rhs)


# * Arithmetic ops

def op_add(func, lhs, rhs):
    return lhs.ret_type.op_add(func, lhs, rhs)


def op_sub(func, lhs, rhs):
    return lhs.ret_type.op_sub(func, lhs, rhs)


def op_div(func, lhs, rhs):
    return lhs.ret_type.op_div(func, lhs, rhs)


def op_mul(func, lhs, rhs):
    return lhs.ret_type.op_mul(func, lhs, rhs)


# * Comparison ops

def op_eq(func, lhs, rhs):
    return lhs.ret_type.op_eq(func, lhs, rhs)


def op_lt(func, lhs, rhs):
    return lhs.ret_type.op_lt(func, lhs, rhs)


def op_gt(func, lhs, rhs):
    return lhs.ret_type.op_gt(func, lhs, rhs)


# TODO/exercise: use enums to represent your ops' names!
# dictionary to relate our ops with our names
operations = {
    "add": op_add,
    "sub": op_sub,
    "div": op_div,
    "mul": op_mul,

    "eq": op_eq,
    "lt": op_lt,
    "gt": op_gt
}
