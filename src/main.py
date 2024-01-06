from llvmlite import binding

from Ast.block import Block
from Ast.constants import NumbericLiteral
from Ast.functions import FuncCall, FuncDef, ReturnStmt
from Ast.ifstatement import IfStmt
from Ast.math import Operation
from Ast.parens import Parens
from Ast.variables import Assignment, VarRef

# llvmlite startup
binding.initialize()
binding.initialize_native_target()
binding.initialize_native_asmprinter()

# Must import this here because of those lines
#  that get the target platform.
from Ast.module import Module


# Code representation of our AST.
"""
def add_nums(x, y):
    return x+y

def main():
    x = 10
    y = 20
    return add_nums(x+y)

def max(x, y):
    if x > y:
        return x
    return y
"""

# The actual AST.
ast = Module(None, "test", "./test", [
    FuncDef(None,
            # Function name
            VarRef(None, "add_nums"),
            # Function args
            Parens(None, [
                VarRef(None, "x"),
                VarRef(None, "y")
            ]),
            # Function Body
            Block(None, [
                ReturnStmt(None,
                           Operation(None,
                                     "add",
                                     VarRef(None, "x"),
                                     VarRef(None, "y")))
            ])),
    FuncDef(None,
            # Function name
            VarRef(None, "main"),
            # Function args (empty args)
            Parens(None),
            # Function Body
            Block(None, [
                # make variable x
                Assignment(None,
                           VarRef(None, "x"),
                           NumbericLiteral(None, 10)),
                # make variable y
                Assignment(None,
                           VarRef(None, "y"),
                           NumbericLiteral(None, 20)),
                # return `add_nums(x, y)`
                ReturnStmt(None,
                           # Call `add_nums`
                           FuncCall(None,
                                    VarRef(None, "add_nums"),
                                    # args
                                    Parens(None, [
                                        VarRef(None, "x"),
                                        VarRef(None, "y")
                                    ])))
            ])),
    FuncDef(None,
            # Function name
            VarRef(None, "max"),
            # Function args
            Parens(None, [
                VarRef(None, "x"),
                VarRef(None, "y")
            ]),
            # Function Body
            Block(None, [
                IfStmt(None,
                       # check x > y
                       Operation(None,
                                 "gt",
                                 VarRef(None, "x"),
                                 VarRef(None, "y")),
                       Block(None, [
                           # return x
                           ReturnStmt(None,
                                      VarRef(None, "x"))
                       ])),
                # return y
                ReturnStmt(None,
                           VarRef(None, "y"))
            ]))
])

ast.pre_eval(None)
ast.eval(None)
