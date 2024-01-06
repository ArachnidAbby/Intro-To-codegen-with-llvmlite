from Ast.basenodes import ASTNode


class IfStmt(ASTNode):
    __slots__ = ("body", "cond", "parent")

    needs_parent = True

    def __init__(self, pos, cond, body):
        super().__init__(pos)

        self.cond = cond
        self.body = body
        self.parent = None

    def pre_eval(self, func):
        if self.cond.needs_parent:
            self.cond.parent = self.parent
        if self.body.needs_parent:
            self.body.parent = self.parent

        self.cond.pre_eval(func)
        self.body.pre_eval(func)

    def eval(self, func):
        current_block = func.builder.block

        # Do nothing if the current block has a terminator (eg: `ret <val>`)
        if current_block.is_terminated:
            return

        # create blocks used for the if stmt
        current_name = current_block.name
        if_block = func.builder.append_basic_block(f"{current_name}.if")
        if_end_block = func.builder.append_basic_block(f"{current_name}.endif")

        # get the i1 necessary for the conditional jump/branch
        cond_typ = self.cond.ret_type
        cond_val = cond_typ.truthy(func, self.cond)

        # conditionally branch
        func.builder.cbranch(cond_val, if_block, if_end_block)

        # evaluate the "true" path of the if-statement
        func.builder.position_at_end(if_block)
        self.body.eval(func)
        if not if_block.is_terminated:
            func.builder.branch(if_end_block)

        # position at the "false" path
        func.builder.position_at_end(if_end_block)
