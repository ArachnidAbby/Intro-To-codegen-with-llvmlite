import errors
from Ast.basenodes import ASTNode, ExpressionNode, VariableInfo


class Assignment(ASTNode):
    __slots__ = ("var_name", "value", "var_type",
                 "parent", "is_declaration")

    needs_parent = True

    def __init__(self, pos, name_node, value_node):
        super().__init__(pos)

        if not name_node.assignable:
            errors.error("Cannot assign to this expression",
                         loc=name_node.position)

        self.var_name = name_node
        self.value = value_node

        # can't determine this because we don't have a parent.
        #  Your parser could pass this in during construction instead of doing
        #  so later. Whatever you would like really.
        self.parent = None
        self.is_declaration = False

        self.var_type = None

    def pre_eval(self, func):
        if self.parent is None:
            errors.error("Cannot do variable assignment outside of a block",
                         loc=self.position)
            return

        if self.var_name.needs_parent:
            self.var_name.parent = self.parent
        if self.value.needs_parent:
            self.value.parent = self.parent

        self.value.pre_eval(func)

        # determine if this is a declaration or not
        if isinstance(self.var_name, VarRef):
            fetched_var = self.parent.get_variable(self.var_name)
            self.is_declaration = fetched_var is None

        # get the type of the variable
        if self.is_declaration:
            self.var_type = self.value.ret_type
        else:
            self.var_name.pre_eval(func)
            self.var_type = self.var_name.ret_type

        # ensure type is the expected type
        # TODO/exercise: do implicit type conversion instead.
        if self.var_type != self.value.ret_type:
            errors.error("Mismatched types during assignment",
                         loc=self.position)

    def eval(self, func):
        if self.var_type is None:
            return
        if self.parent is None:
            return

        if self.is_declaration:
            self.parent.make_variable(func, self.var_name, self.var_type)

        # use asttype's `store` method.
        self.var_type.store(func, self.var_name, self.value)


class VarRef(ExpressionNode):
    __slots__ = ("var_name", "parent", "var_info")

    needs_parent = True
    assignable = True

    def __init__(self, pos, var_name):
        super().__init__(pos)

        self.var_name = var_name
        self.parent = None
        self.var_info = None

    def pre_eval(self, func):
        # the parent to this node should only be None if we
        #  did something wrong!
        if self.parent is None:
            errors.error("Cannot do a variable reference at a top level",
                         loc=self.position)
            return

        self.var_info = self.parent.get_variable(self)

        if self.var_info is not None:
            self.ret_type = self.var_info.ret_type

    def eval(self, func):
        # Error if we couldn't find the var
        ptr = self.as_ptr(func)

        return func.builder.load(ptr)

    def as_ptr(self, func):
        if self.var_info is None and self.parent is not None:
            self.var_info = self.parent.get_variable(self)

        if self.var_info is None:
            errors.error(f"Cannot find variable: '{self.var_name}' in " +
                         "current scope",
                         loc=self.position)
            return

        if self.var_info.is_function:
            errors.error("Function cannot be used as a value")

        self._ptr = self.var_info.ptr
        return self._ptr
