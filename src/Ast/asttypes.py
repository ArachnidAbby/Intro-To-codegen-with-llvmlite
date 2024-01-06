from typing import Optional, Self

from llvmlite import ir

import errors


# The base type class here. Mocks up all of our expected behavior
#  It also adds default implementation to automatically add errors.
class Type:
    __slots__ = ()

    # Useful properties a type can have
    name = "UNKNOWN/UNQUALIFIED TYPE"
    ir_type: ir.Type | None = None  # the llvm type

    def __init__(self):
        pass

    # * Unused for this talk, there is only 1 type.
    def convert_from(self, func, node, other_type: Self):
        errors.error(f"{self} has no conversions")

    # * Unused for this talk
    @property
    def pass_by_pointer(self):
        return False

    def get_op_return(self, func, op_name, lhs, rhs) -> Optional[Self]:
        errors.error("Operation is not supported")
        return None

    # * Arithmetic

    def op_add(self, func, lhs, rhs) -> Optional[ir.Instruction]:
        errors.error("Operation '+' is not supported")
        return None

    def op_sub(self, func, lhs, rhs) -> Optional[ir.Instruction]:
        errors.error("Operation '-' is not supported")
        return None

    def op_div(self, func, lhs, rhs) -> Optional[ir.Instruction]:
        errors.error("Operation '/' is not supported")
        return None

    def op_mul(self, func, lhs, rhs) -> Optional[ir.Instruction]:
        errors.error("Operation '*' is not supported")
        return None

    # * Comparison

    def op_eq(self, func, lhs, rhs) -> Optional[ir.Instruction]:
        errors.error("Operation '==' is not supported")
        return None

    def op_lt(self, func, lhs, rhs) -> Optional[ir.Instruction]:
        errors.error("Operation '<' is not supported")
        return None

    def op_gt(self, func, lhs, rhs) -> Optional[ir.Instruction]:
        errors.error("Operation '>' is not supported")
        return None

    # * Weird Special stuff

    # checking if a value is true or false
    def truthy(self, func, value) -> Optional[ir.Instruction | ir.Constant]:
        return ir.Constant(ir.IntType(1), 0)

    # * 'loc' is the place we store it.
    # *  This is only a variable reference right now.
    def store(self, func, loc, value):
        return func.builder.store(value.eval(func), loc.as_ptr(func))

    # should make this more complicated for things
    #  like struct types or tuples
    def __eq__(self, other):
        return self.name == other.name


class NumberType(Type):
    __slots__ = ()

    name = "i64"

    # Interestingly, llvm makes no distinction between signed/unsigned ints
    ir_type = ir.IntType(64)

    def get_op_return(self, func, op_name, lhs, rhs) -> Optional[Self]:
        match op_name:
            case "add" | "sub" | "div" | "mul":
                # * you could want complex logic here if using multiple number types.
                # *  Like a float being added to an int should return a float
                return self
            case "eq" | "lt" | "gt":
                return self
            case _:
                errors.error("Operation not supported for the 'Number' type")
                return None

    # * Arithmetic

    def op_add(self, func, lhs, rhs) -> ir.Instruction:
        lhs_evaled = lhs.eval(func)
        rhs_evaled = rhs.eval(func)

        return func.builder.add(lhs_evaled, rhs_evaled)

    def op_sub(self, func, lhs, rhs) -> ir.Instruction:
        lhs_evaled = lhs.eval(func)
        rhs_evaled = rhs.eval(func)

        return func.builder.sub(lhs_evaled, rhs_evaled)

    # ! Division by zero can still occur. This can cause an error.
    # !  how should the compiler handle it? Up to you!
    def op_div(self, func, lhs, rhs) -> ir.Instruction:
        lhs_evaled = lhs.eval(func)
        rhs_evaled = rhs.eval(func)

        # "signed" division (hence `sdiv``)
        return func.builder.sdiv(lhs_evaled, rhs_evaled)

    def op_mul(self, func, lhs, rhs) -> ir.Instruction:
        lhs_evaled = lhs.eval(func)
        rhs_evaled = rhs.eval(func)

        return func.builder.mul(lhs_evaled, rhs_evaled)

    # * Comparison

    # TODO/exercise: make a bool type instead of casting back to i64!

    def op_eq(self, func, lhs, rhs) -> ir.Instruction:
        lhs_evaled = lhs.eval(func)
        rhs_evaled = rhs.eval(func)

        # int comparison (signed).
        val = func.builder.icmp_signed("==", lhs_evaled, rhs_evaled)

        # turn this back into an i64
        return func.builder.zext(val, self.ir_type)

    def op_lt(self, func, lhs, rhs) -> ir.Instruction:
        lhs_evaled = lhs.eval(func)
        rhs_evaled = rhs.eval(func)

        # int comparison (signed).
        val = func.builder.icmp_signed("<", lhs_evaled, rhs_evaled)

        # turn this back into an i64
        return func.builder.zext(val, self.ir_type)

    def op_gt(self, func, lhs, rhs) -> ir.Instruction:
        lhs_evaled = lhs.eval(func)
        rhs_evaled = rhs.eval(func)

        # int comparison (signed).
        val = func.builder.icmp_signed(">", lhs_evaled, rhs_evaled)

        # turn this back into an i64
        return func.builder.zext(val, self.ir_type)

    # * Weird Special stuff

    # checking if a value is true or false
    def truthy(self, func, value) -> ir.Instruction:
        zero = ir.Constant(self.ir_type, 0)
        return func.builder.icmp_signed("!=", value.eval(func), zero)
