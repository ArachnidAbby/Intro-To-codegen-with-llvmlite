from llvmlite import binding, ir

from Ast.basenodes import ASTNode, VariableInfo

# ! things that will be useful for you later
# !  they are useless right now.
target = binding.Target.from_default_triple()
target_machine = target.create_target_machine()


class Module(ASTNode):
    __slots__ = ("body", "mod_name", "location", "globals",
                 "ir_mod")

    def __init__(self, pos, name, loc, body):
        super().__init__(pos)

        self.mod_name = name
        self.location = loc
        self.globals = {}

        for child in body:
            if child.needs_parent:
                child.parent = self

        self.body = body
        self.ir_mod = ir.Module(name=name)

    def get_unique_name(self, name: str) -> str:
        # ! Don't want to mangle our main functions name
        if name == "main":
            return name

        return self.ir_mod.get_unique_name(f"{self.mod_name}.{name}")

    # * make a function
    def make_function(self, func_name, ir_func):
        var_info = VariableInfo(func_name.var_name, None, ir_func, True)

        self.globals[func_name.var_name] = var_info
        return var_info

    def get_variable(self, var_node):
        var_name = var_node.var_name

        if var_name in self.globals:
            return self.globals[var_name]

    # func shouldn't have a value here.
    def pre_eval(self, func=None):
        for child in self.body:
            child.pre_eval(self)

    # func shouldn't have a value here.
    def eval(self, func=None):
        for child in self.body:
            child.eval(self)

        # simply printing the module into the console
        print(self.ir_mod)
