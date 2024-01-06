# Introduction to Codegen with llvmlite

This is a small introduction to how an AST would use llvmlite to
generate llvm-ir (llir).

This is *technically* turing complete (I think). It is missing features a language would likely want.

There are of course *several* `TODO/exercise` comments left in the code as challenges for the
reader.

> This was shared on the `Compilers and Interpreters` discord server on `01/06/2024 (M/D/Y)`
> If you see this before that date, come join us to learn more!

## Requirements

- python 3.11.x (uses a 3.11 features + a feature that was removed in 3.12)
- pip (do `pip install -r requirements.txt`)

## Things not included here

These things are intentionally not included in this example.

- Lexing
- Parsing
- Emitting to a file
- Identified Struct types
- "Advanced" llvm instructions like `gep` or `phi`
- Type checking (there is only 1 type present)
- Optimization passes
- JIT / the execution engine
- Emiting object file
- Linking (to create an executable)

## Instructions covered

- `icmp` (`>`, `<`, & `==`. `!=` also kind-of used)
- `alloca`
- `store`
- `ret` (but not `ret void`)
- `load`
- `br` (cbranch and branch)
- `add`
- `sub`
- `mul`
- `sdiv`
- `zext`
- Function definition
- Creating blocks & positioning.
- Doing all allocations at the start of a function.
- An extremely basic Type system that includes `1` type.

## Additional resources.

- [Compilers and Interpreters discord (Invite)](https://discord.gg/7DdxXWczYS)
- [llvmlite docs: user-guide](https://llvmlite.readthedocs.io/en/latest/user-guide/index.html)
- [Mapping High-level Constructs to LLVM-IR](https://mapping-high-level-constructs-to-llvm-ir.readthedocs.io/en/latest/)

- *This is useful for those unaffiliated with ANSI* <br>
[Info about ANSI escape codes](https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html)

- *LLVM has bad documentation in my experience* <br>
[LLVM language reference](https://llvm.org/docs/LangRef.html)
- [What is SSA](https://en.wikipedia.org/wiki/Static_single-assignment_form)
- *This explains `__slots__`. Most people don't know about this python feature* <br>
[What is `__slots__`](https://wiki.python.org/moin/UsingSlots)
- *A little self-plug, but I do use llvmlite here. Please consider starring the project!* <br>
[BCL](https://github.com/spidertyler2005/BCL)

## Reuse of this code

If you wish to reuse this code, you may do so. The only thing I ask is that
you credit me on your project's readme or wherever it makes sense
to add the attribution.