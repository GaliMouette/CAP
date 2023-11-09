from typing import List, Tuple
from MiniCVisitor import MiniCVisitor
from MiniCParser import MiniCParser
from Lib.LinearCode import LinearCode
from Lib import RiscV
from Lib.RiscV import Condition
from Lib import Operands
from antlr4.tree.Trees import Trees
from Lib.Errors import MiniCInternalError, MiniCUnsupportedError

"""
CAP, MIF08, three-address code generation + simple alloc
This visitor constructs an object of type "LinearCode".
"""


class MiniCCodeGen3AVisitor(MiniCVisitor):

    _current_function: LinearCode

    def __init__(self, debug, parser):
        super().__init__()
        self._parser = parser
        self._debug = debug
        self._functions = []
        self._lastlabel = ""

    def get_functions(self) -> List[LinearCode]:
        return self._functions

    def printSymbolTable(self):  # pragma: no cover
        print("--variables to temporaries map--")
        for keys, values in self._symbol_table.items():
            print(keys + '-->' + str(values))

    # handle variable decl

    def visitVarDecl(self, ctx) -> None:
        type_str = ctx.typee().getText()
        vars_l = self.visit(ctx.id_l())
        for name in vars_l:
            if name in self._symbol_table:
                raise MiniCInternalError(
                    "Variable {} has already been declared".format(name))
            else:
                tmp = self._current_function.fdata.fresh_tmp()
                self._symbol_table[name] = tmp
                if type_str not in ("int", "bool"):
                    raise MiniCUnsupportedError("Unsupported type " + type_str)
                # Initialization to 0 or False, both represented with 0
                self._current_function.add_instruction(
                    RiscV.li(tmp, Operands.Immediate(0)))

    def visitIdList(self, ctx) -> List[str]:
        t = self.visit(ctx.id_l())
        t.append(ctx.ID().getText())
        return t

    def visitIdListBase(self, ctx) -> List[str]:
        return [ctx.ID().getText()]

    # expressions

    def visitParExpr(self, ctx) -> Operands.Temporary:
        return self.visit(ctx.expr())

    def visitIntAtom(self, ctx) -> Operands.Temporary:
        val = Operands.Immediate(int(ctx.getText()))
        dest = self._current_function.fdata.fresh_tmp()
        self._current_function.add_instruction(RiscV.li(dest, val))
        return dest

    def visitFloatAtom(self, ctx) -> Operands.Temporary:
        raise MiniCUnsupportedError("float literal")

    def visitBooleanAtom(self, ctx) -> Operands.Temporary:
        # true is 1 false is 0
        if ctx.TRUE() is not None:
            val = Operands.Immediate(1)
        elif ctx.FALSE() is not None:
            val = Operands.Immediate(0)
        else:
            raise MiniCInternalError("Unknown boolean atom")
        dest = self._current_function.fdata.fresh_tmp()
        self._current_function.add_instruction(RiscV.li(dest, val))
        return dest

    def visitIdAtom(self, ctx) -> Operands.Temporary:
        try:
            # get the temporary associated to id
            return self._symbol_table[ctx.getText()]
        except KeyError:  # pragma: no cover
            raise MiniCInternalError(
                "Undefined variable {}, this should have failed to typecheck."
                .format(ctx.getText())
            )

    def visitStringAtom(self, ctx) -> Operands.Temporary:
        raise MiniCUnsupportedError("string atom")

    # now visit expressions

    def visitAtomExpr(self, ctx) -> Operands.Temporary:
        return self.visit(ctx.atom())

    def visitAdditiveExpr(self, ctx) -> Operands.Temporary:
        assert ctx.myop is not None
        tmpl: Operands.Temporary = self.visit(ctx.expr(0))
        tmpr: Operands.Temporary = self.visit(ctx.expr(1))
        if ctx.myop.type == MiniCParser.PLUS:
            op = RiscV.add
        elif ctx.myop.type == MiniCParser.MINUS:
            op = RiscV.sub
        else:
            raise MiniCInternalError("Unknown additive operator")
        dest = self._current_function.fdata.fresh_tmp()
        self._current_function.add_instruction(op(dest, tmpl, tmpr))
        return dest

    def visitOrExpr(self, ctx) -> Operands.Temporary:
        op = RiscV.lor
        tmpl: Operands.Temporary = self.visit(ctx.expr(0))
        tmpr: Operands.Temporary = self.visit(ctx.expr(1))
        dest = self._current_function.fdata.fresh_tmp()
        self._current_function.add_instruction(op(dest, tmpl, tmpr))
        return dest

    def visitAndExpr(self, ctx) -> Operands.Temporary:
        op = RiscV.land
        tmpl: Operands.Temporary = self.visit(ctx.expr(0))
        tmpr: Operands.Temporary = self.visit(ctx.expr(1))
        dest = self._current_function.fdata.fresh_tmp()
        self._current_function.add_instruction(op(dest, tmpl, tmpr))
        return dest

    def visitEqualityExpr(self, ctx) -> Operands.Temporary:
        return self.visitRelationalExpr(ctx)

    def visitRelationalExpr(self, ctx) -> Operands.Temporary:
        assert ctx.myop is not None
        c = Condition(ctx.myop.type)
        if self._debug: # pragma: no cover
            print("relational expression:")
            print(Trees.toStringTree(ctx, [], self._parser))
            print("Condition:", c)
        tmpl: Operands.Temporary = self.visit(ctx.expr(0))
        tmpr: Operands.Temporary = self.visit(ctx.expr(1))
        dest = self._current_function.fdata.fresh_tmp()
        imm0 = Operands.Immediate(0)
        imm1 = Operands.Immediate(1)
        endl = self._current_function.fdata.fresh_label('end_rel_expr')
        self._current_function.add_instruction(RiscV.li(dest, imm0))
        jump = RiscV.conditional_jump(endl, tmpl, c.negate(), tmpr)
        self._current_function.add_instruction(jump)
        self._current_function.add_instruction(RiscV.li(dest, imm1))
        self._current_function.add_label(endl)
        return dest

    def visitMultiplicativeExpr(self, ctx) -> Operands.Temporary:
        assert ctx.myop is not None

        div_by_zero_lbl = self._current_function.fdata.get_label_div_by_zero()

        tmpl: Operands.Temporary = self.visit(ctx.expr(0))
        tmpr: Operands.Temporary = self.visit(ctx.expr(1))
        dest = self._current_function.fdata.fresh_tmp()

        op_type = {MiniCParser.MULT: RiscV.mul, MiniCParser.DIV: RiscV.div, MiniCParser.MOD: RiscV.rem}
        if ctx.myop.type not in op_type:
            raise MiniCInternalError("Unknown multiplicative operator")

        if ctx.myop.type == MiniCParser.DIV or ctx.myop.type == MiniCParser.MOD:
            imm0= Operands.Immediate(0)
            zero = self._current_function.fdata.fresh_tmp()
            self._current_function.add_instruction(RiscV.li(zero, imm0))

            jump = RiscV.conditional_jump
            cond = Condition(MiniCParser.EQ)
            self._current_function.add_instruction(jump(div_by_zero_lbl, tmpr, cond, zero))

        op = op_type[ctx.myop.type]
        self._current_function.add_instruction(op(dest, tmpl, tmpr))
        return dest

    def visitNotExpr(self, ctx) -> Operands.Temporary:
        tmp: Operands.Temporary = self.visit(ctx.expr())
        # 1 is loaded in a temporary because sub does not support immediate
        imm1 = Operands.Immediate(1)
        one = self._current_function.fdata.fresh_tmp()
        self._current_function.add_instruction(RiscV.li(one, imm1))
        dest = self._current_function.fdata.fresh_tmp()
        # Use sub 1 - x because not doest not exist
        self._current_function.add_instruction(RiscV.sub(dest, one, tmp))
        return dest

    def visitUnaryMinusExpr(self, ctx) -> Operands.Temporary:
        tmp = self.visit(ctx.expr())
        # 0 is loaded in a temporary because sub does not support immediate
        imm0 = Operands.Immediate(0)
        zero = self._current_function.fdata.fresh_tmp()
        self._current_function.add_instruction(RiscV.li(zero, imm0))
        dest = self._current_function.fdata.fresh_tmp()
        self._current_function.add_instruction(RiscV.sub(dest, zero, tmp))
        return dest

    def visitProgRule(self, ctx) -> None:
        self.visitChildren(ctx)

    def visitFuncDef(self, ctx) -> None:
        funcname = ctx.ID().getText()
        self._current_function = LinearCode(funcname)
        self._symbol_table = dict()

        self.visit(ctx.vardecl_l())
        self.visit(ctx.block())
        self._current_function.add_comment("Return at end of function:")
        # This skeleton doesn't deal properly with functions, and
        # hardcodes a "return 0;" at the end of function. Generate
        # code for this "return 0;".
        self._current_function.add_instruction(
        	RiscV.li(Operands.A0, Operands.Immediate(0)))
        self._functions.append(self._current_function)
        del self._current_function

    def visitAssignStat(self, ctx) -> None:
        if self._debug: # pragma: no cover
            print("assign statement, rightexpression is:")
            print(Trees.toStringTree(ctx.expr(), [], self._parser))
        expr_temp = self.visit(ctx.expr())
        name = ctx.ID().getText()
        self._current_function.add_instruction(RiscV.mv(self._symbol_table[name], expr_temp))

    def visitIfStat(self, ctx) -> None:
        if self._debug: # pragma: no cover
            print("if statement, condition is")
            print(Trees.toStringTree(ctx.expr(), None, self._parser))
            print("and block is:")
            print(Trees.toStringTree(ctx.then_block, None, self._parser))
            if ctx.else_block is not None:
                print("else block is:")
                print(Trees.toStringTree(ctx.else_block, None, self._parser))
        end_if_label = self._current_function.fdata.fresh_label("end_if")
        else_label = self._current_function.fdata.fresh_label("else")

        tmp = self.visit(ctx.expr())

        jump = RiscV.conditional_jump
        cond = Condition(MiniCParser.EQ)
        imm0 = Operands.Immediate(0)
        zero = self._current_function.fdata.fresh_tmp()
        self._current_function.add_instruction(RiscV.li(zero, imm0))
        self._current_function.add_instruction(jump(else_label, tmp, cond, zero))

        self.visit(ctx.then_block)
        self._current_function.add_instruction(RiscV.jump(end_if_label))

        self._current_function.add_label(else_label)
        if ctx.else_block is not None:
            self.visit(ctx.else_block)

        self._current_function.add_label(end_if_label)

    def visitWhileStat(self, ctx) -> None:
        if self._debug: # pragma: no cover
            print("while statement, condition is:")
            print(Trees.toStringTree(ctx.expr(), [], self._parser))
            print("and block is:")
            print(Trees.toStringTree(ctx.stat_block(), None, self._parser))
        loop_label = self._current_function.fdata.fresh_label("loop")
        end_loop_label = self._current_function.fdata.fresh_label("end_loop")

        self._current_function.add_label(loop_label)

        tmp = self.visit(ctx.expr())

        jump = RiscV.conditional_jump
        cond = Condition(MiniCParser.EQ)
        imm0 = Operands.Immediate(0)
        zero = self._current_function.fdata.fresh_tmp()
        self._current_function.add_instruction(RiscV.li(zero, imm0))
        self._current_function.add_instruction(jump(end_loop_label, tmp, cond, zero))

        self.visit(ctx.stat_block())

        self._current_function.add_instruction(RiscV.jump(loop_label))

        self._current_function.add_label(end_loop_label)

    # visit statements

    def visitPrintlnintStat(self, ctx) -> None:
        expr_loc = self.visit(ctx.expr())
        if self._debug: # pragma: no cover
            print("print_int statement, expression is:")
            print(Trees.toStringTree(ctx.expr(), [], self._parser))
        self._current_function.add_instruction_PRINTLN_INT(expr_loc)

    def visitPrintlnboolStat(self, ctx) -> None:
        expr_loc = self.visit(ctx.expr())
        self._current_function.add_instruction_PRINTLN_INT(expr_loc)

    def visitPrintlnfloatStat(self, ctx) -> None:
        raise MiniCUnsupportedError("Unsupported type float")

    def visitPrintlnstringStat(self, ctx) -> None:
        raise MiniCUnsupportedError("Unsupported type string")

    def visitStatList(self, ctx) -> None:
        for stat in ctx.stat():
            self._current_function.add_comment(Trees.toStringTree(stat, [], self._parser))
            self.visit(stat)

    def visitForStat(self, ctx):
        loop_label = self._current_function.fdata.fresh_label("loop")
        end_loop_label = self._current_function.fdata.fresh_label("end_loop")

        if ctx.init is not None:
            self.visit(ctx.init)

        self._current_function.add_label(loop_label)


        tmp = self.visit(ctx.cond) if ctx.cond is not None else None

        if tmp is not None:
            jump = RiscV.conditional_jump
            cond = Condition(MiniCParser.EQ)
            imm0 = Operands.Immediate(0)
            zero = self._current_function.fdata.fresh_tmp()
            self._current_function.add_instruction(RiscV.li(zero, imm0))
            self._current_function.add_instruction(jump(end_loop_label, tmp, cond, zero))

        self.visit(ctx.body)

        if ctx.inc is not None:
            self.visit(ctx.inc)

        self._current_function.add_instruction(RiscV.jump(loop_label))

        self._current_function.add_label(end_loop_label)
