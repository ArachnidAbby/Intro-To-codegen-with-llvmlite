from llvmlite import ir

from Ast.asttypes import NumberType
from Ast.basenodes import ExpressionNode


class NumbericLiteral(ExpressionNode):
    __slots__ = ("value",)

    def __init__(self, pos, value: int):
        super().__init__(pos)
        self.value = value
        self.ret_type = NumberType()

    # we don't really want to do anything here!
    def pre_eval(self, func):
        pass

    def eval(self, func) -> ir.Constant:
        typ = self.ret_type.ir_type  # the ir_type (i64) of our Number type
        return ir.Constant(typ, self.value)
