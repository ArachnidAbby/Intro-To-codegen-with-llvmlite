from Ast.basenodes import ExpressionNode


# Anything wrapped in `()`
class Parens(ExpressionNode):
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

        if len(self.children) == 1:
            self.ret_type = self.evaled_children[0]

    def eval(self, func):
        for child in self:
            val = child.eval(func)
            self.evaled_children.append(val)

        # return contents if this is a single element parenth block
        #  useful ex: `8 * (7 + 1)`
        if len(self.children) == 1:
            return self.evaled_children[0]

        # TODO/exercise: Create a tuple datatype and instantiate it here!
