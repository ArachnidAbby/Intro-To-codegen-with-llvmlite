# The most simple nodes possible. These are the basis for all other nodes.
# These define default behaviors and overall structure.

from typing import NamedTuple, Optional

from llvmlite import ir

import errors

from .asttypes import Type

# (line, char, span, file: str)
srcPosition = tuple[int, int, int, str]


# * Combine together several source positions into a single one.
def merge_src_positions(positions: list[srcPosition]) -> srcPosition:
    # TODO/exercise: implement this for your compiler.
    # TODO/exercise:  This example has no parser or src positions!
    return positions[0]


class VariableInfo(NamedTuple):
    var_name: str
    ret_type: Type
    ptr: ir.Instruction | ir.AllocaInstr | ir.Function

    # It is recommended to actually use a Function type.
    #  This makes things like the `.` operator easier
    #  In whatever language you are making. This is what I do
    #  in my lang.
    is_function: bool


# ? You may want this to be an Abstract Base Class. You decide!
class ASTNode:
    __slots__ = ("_pos",)

    # useful properties
    needs_parent = False

    def __init__(self, pos: srcPosition):
        self._pos = pos

    # * Multiple passes thru the AST.
    # *  You could want more too!
    # *  Commonly you have 1-2 (or more) for symbol declaration
    def pre_eval(self, func):
        pass

    def eval(self, func) -> Optional[ir.Instruction]:
        pass

    # Should be overwritten when you want to merge together positions.
    @property
    def position(self) -> srcPosition:
        return self._pos


class ExpressionNode(ASTNode):
    __slots__ = ("ret_type", "_ptr")

    # Important properties
    assignable = False

    def __init__(self, pos):
        super().__init__(pos)

        self.ret_type = None
        self._ptr = None

    # get a pointer to the thing the node refers to
    def as_ptr(self, func) -> Optional[ir.Instruction]:
        if self._ptr is None:
            self._ptr = func.create_temp_var(self.ret_type)
            val = self.eval(func)
            func.builder.store(val, self._ptr)

        return self._ptr

    # * We won't implement this right now
    def get_as_type(self, func) -> Optional[Type]:
        errors.error("Not a valid type signature", loc=self.position)
        return None
