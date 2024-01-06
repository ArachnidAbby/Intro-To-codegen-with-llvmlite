from typing import Optional

from llvmlite import ir

import errors
from Ast.asttypes import NumberType
from Ast.basenodes import ASTNode, ExpressionNode, VariableInfo
from Ast.variables import VarRef


class FuncDef(ASTNode):
    __slots__ = ("builder", "func_name", "parent", "body", "parens",
                 "variables", "func_ir", "func_ty", "start_block")

    needs_parent = True  # this makes self.parent the current module!

    def __init__(self, pos, name, args, body):
        super().__init__(pos)

        self.builder = None
        self.parent = None
        self.func_ir = None
        self.func_ty = None
        self.start_block = None
        self.parens = args
        self.func_name = name
        self.variables = {}
        self.body = body

        if not isinstance(name, VarRef):
            errors.error("Function name must be a valid variable-style name.",
                         loc=name.position)

        # body should always be a `Block`.
        body.parent = self

    def alloc_variable(self, name, typ):
        if self.builder is None:
            return

        # * We only want to have allocations at the top
        # *  We don't want to accidentally allocate in a loop or something
        # TODO/exercise: look into using `builder.goto_entry_block(block)`
        current_block = self.builder.block
        self.builder.position_at_start(self.start_block)
        ptr = self.builder.alloca(typ.ir_type, name=name)
        self.builder.position_at_end(current_block)
        return ptr

    def create_temp_var(self, typ):
        return self.alloc_variable("TMP_VAR", typ)

    def get_variable(self, name):
        var_name = name.var_name

        if var_name in self.variables.keys():
            return self.variables[var_name]
        if self.parent is not None:
            return self.parent.get_variable(name)

    def _alloc_arguments(self):
        if self.builder is None or self.func_ir is None:
            return

        # To make our args function as normal variables,
        #  We must allocate them into memory. This makes them mutable
        for val, var_node in zip(self.func_ir.args, self.parens):
            var_name = var_node.var_name
            ptr = self.alloc_variable(var_name, NumberType)
            self.builder.store(val, ptr)
            info = VariableInfo(var_name, NumberType(), ptr, False)
            self.variables[var_name] = info

    def pre_eval(self, func):
        if self.parent is None:
            errors.error("This function is somehow not part of a module!?!",
                         loc=self.position)
            return

        # * Hint for exercise: Create a new KeyValuePair node for this
        # TODO/exercise: Make the AST use the real type of each argument

        # assume all arguments are i64. We only have one type right now!
        arg_types = [NumberType.ir_type for _ in self.parens]

        # TODO/exercise: Make AST take into account return type
        self.func_ty = ir.FunctionType(NumberType.ir_type, arg_types)
        unique_name = self.parent.get_unique_name(self.func_name.var_name)
        self.func_ir = ir.Function(self.parent.ir_mod, self.func_ty,
                                   name=unique_name)
        self.parent.make_function(self.func_name, self.func_ir)

        # the first block in our function will always be run by default
        self.start_block = self.func_ir.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(self.start_block)
        self._alloc_arguments()

        self.body.pre_eval(self)

    def eval(self, func):
        if self.builder is None:
            return

        self.body.eval(self)

        # Have a default return if the block is not terminated
        current_block = self.builder.block
        if current_block is not None and not current_block.is_terminated:
            zero = ir.Constant(NumberType.ir_type, 0)
            self.builder.ret(zero)


class FuncCall(ExpressionNode):
    __slots__ = ("func_name", "args", "parent", "func_info")

    needs_parent = True

    def __init__(self, pos, func_name, args):
        super().__init__(pos)

        self.parent = None
        self.func_name = func_name
        self.args = args
        self.func_info = None

    def pre_eval(self, func):
        if self.parent is None:
            errors.error("Unable to call functions at a top-level",
                         loc=self.position)
            return

        if self.func_name.needs_parent:
            self.func_name.parent = self.parent
        if self.args.needs_parent:
            self.args.parent = self.parent

        self.args.pre_eval(func)
        self.func_info = self.parent.get_variable(self.func_name)
        self.ret_type = NumberType()
        if self.func_info is None or not self.func_info.is_function:
            errors.error("Function not found",
                         loc=self.func_name.position)
        # TODO/exercise: make a way to check the arguments of the funcs
        # TODO/exercise:  To see if they match
        ...

    def eval(self, func) -> Optional[ir.Instruction]:
        if self.func_info is None:
            return None
        self.args.eval(func)
        return func.builder.call(self.func_info.ptr, self.args.evaled_children)


class ReturnStmt(ASTNode):
    __slots__ = ("value", "parent")

    needs_parent = True

    def __init__(self, pos, value):
        super().__init__(pos)
        self.parent = None
        self.value = value

    def pre_eval(self, func):
        if self.value.needs_parent:
            self.value.parent = self.parent

        self.value.pre_eval(func)

        # TODO/exercise: implement type checking.
        ...

    def eval(self, func):
        func.builder.ret(self.value.eval(func))
