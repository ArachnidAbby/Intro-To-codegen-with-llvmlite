from typing import Optional

from .basenodes import ASTNode, VariableInfo


# Blocks surrounded by `{}`
class Block(ASTNode):
    __slots__ = ("children", "variables", "parent")

    needs_parent = True

    def __init__(self, pos, children=None):
        super().__init__(pos)

        if children is None:
            self.children = []
        else:
            # Handle the nesting
            for child in children:
                if child.needs_parent:
                    child.parent = self
            self.children = children

        self.variables = {}
        self.parent = None

    def __iter__(self):
        yield from self.children

    def get_variable(self, var_node) -> Optional[VariableInfo]:
        var_name = var_node.var_name
        if var_name in self.variables.keys():
            return self.variables[var_name]

        if self.parent is not None:
            return self.parent.get_variable(var_node)
        return None

    def make_variable(self, func, var_node, typ) -> Optional[VariableInfo]:
        var_name = var_node.var_name
        var_ptr = func.alloc_variable(var_name, typ)

        var = VariableInfo(var_name, typ, var_ptr, False)
        self.variables[var_name] = var

        return var

    def pre_eval(self, func):
        for child in self:
            child.pre_eval(func)

    def eval(self, func):
        for child in self:
            child.eval(func)
