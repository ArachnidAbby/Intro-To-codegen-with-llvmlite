from Ast.basenodes import ASTNode


class Parens(ASTNode):
    __slots__ = ("children", "evaled_children", "parent")

    needs_parent = True

    def __init__(self, pos, children=None):
        super().__init__(pos)

        if children is None:
            self.children = []
        else:
            self.children = children

        self.evaled_children = []
        self.parent = None

    def __iter__(self):
        yield from self.children

    def pre_eval(self, func):
        for child in self:
            if child.needs_parent:
                child.parent = self.parent
            child.pre_eval(func)

    def eval(self, func):
        for child in self:
            val = child.eval(func)
            self.evaled_children.append(val)
