# Visitor to *typecheck* MiniC files
from typing import List, NoReturn
from MiniCVisitor import MiniCVisitor
from MiniCParser import MiniCParser
from Lib.Errors import MiniCInternalError, MiniCTypeError

from enum import Enum


class BaseType(Enum):
    Float, Integer, Boolean, String = range(4)


# Basic Type Checking for MiniC programs.
class MiniCTypingVisitor(MiniCVisitor):

    def __init__(self):
        self._memorytypes = dict()  # id -> types
        # For now, we don't have real functions ...
        self._current_function = "main"

    def _raise(self, ctx, for_what, *types):
        raise MiniCTypeError(
            'In function {}: Line {} col {}: invalid type for {}: {}'.format(
                self._current_function,
                ctx.start.line, ctx.start.column, for_what,
                ' and '.join(t.name.lower() for t in types)))

    def _assertSameType(self, ctx, for_what, *types):
        if not all(types[0] == t for t in types):
            raise MiniCTypeError(
                'In function {}: Line {} col {}: type mismatch for {}: {}'.format(
                    self._current_function,
                    ctx.start.line, ctx.start.column, for_what,
                    ' and '.join(t.name.lower() for t in types)))

    def _raiseNonType(self, ctx, message) -> NoReturn:
        raise MiniCTypeError(
            'In function {}: Line {} col {}: {}'.format(
                self._current_function,
                ctx.start.line, ctx.start.column, message))

    # type declaration

    def visitVarDecl(self, ctx) -> None:
        typee = self.visit(ctx.typee())
        for var in self.visit(ctx.id_l()):
            if var in self._memorytypes:
                self._raiseNonType(ctx, "Variable {} already declared".format(
                    var))
            self._memorytypes[var] = typee

    def visitBasicType(self, ctx):
        assert ctx.mytype is not None
        if ctx.mytype.type == MiniCParser.INTTYPE:
            return BaseType.Integer
        elif ctx.mytype.type == MiniCParser.FLOATTYPE:
            return BaseType.Float
        elif ctx.mytype.type == MiniCParser.BOOLTYPE:
            return BaseType.Boolean
        elif ctx.mytype.type == MiniCParser.STRINGTYPE:
            return BaseType.String

    def visitIdList(self, ctx) -> List[str]:
        return self.visitIdListBase(ctx) + self.visit(ctx.id_l())

    def visitIdListBase(self, ctx) -> List[str]:
        return [ctx.ID().getText()]

    # typing visitors for expressions, statements !

    # visitors for atoms --> type
    def visitParExpr(self, ctx):
        return self.visit(ctx.expr())

    def visitIntAtom(self, ctx):
        return BaseType.Integer

    def visitFloatAtom(self, ctx):
        return BaseType.Float

    def visitBooleanAtom(self, ctx):
        return BaseType.Boolean

    def visitIdAtom(self, ctx):
        try:
            return self._memorytypes[ctx.getText()]
        except KeyError:
            self._raiseNonType(ctx,
                               "Undefined variable {}".format(ctx.getText()))

    def visitStringAtom(self, ctx):
        return BaseType.String

    # now visit expr

    def visitAtomExpr(self, ctx):
        return self.visit(ctx.atom())

    def visitOrExpr(self, ctx):
        ltype = self.visit(ctx.expr(0))
        rtype = self.visit(ctx.expr(1))
        if ltype == rtype == BaseType.Boolean:
            return BaseType.Boolean
        self._raise(ctx, 'or operands', ltype, rtype)

    def visitAndExpr(self, ctx):
        ltype = self.visit(ctx.expr(0))
        rtype = self.visit(ctx.expr(1))
        if ltype == rtype == BaseType.Boolean:
            return BaseType.Boolean
        self._raise(ctx, 'and operands', ltype, rtype)

    def visitEqualityExpr(self, ctx):
        ltype = self.visit(ctx.expr(0))
        rtype = self.visit(ctx.expr(1))
        self._assertSameType(ctx, 'equality operands', ltype, rtype)
        return BaseType.Boolean

    def visitRelationalExpr(self, ctx):
        ltype = self.visit(ctx.expr(0))
        rtype = self.visit(ctx.expr(1))
        if ltype == rtype == BaseType.Integer:
            return BaseType.Boolean
        elif ltype == rtype == BaseType.Float:
            return BaseType.Boolean
        self._raise(ctx, 'relational operands', ltype, rtype)

    def visitAdditiveExpr(self, ctx):
        assert ctx.myop is not None
        ltype = self.visit(ctx.expr(0))
        rtype = self.visit(ctx.expr(1))
        if ltype == rtype == BaseType.Integer:
            return BaseType.Integer
        elif ltype == rtype == BaseType.Float:
            return BaseType.Float
        elif ctx.myop.type == MiniCParser.PLUS  and ltype == rtype == BaseType.String:
            return BaseType.String
        self._raise(ctx, 'additive operands', ltype, rtype)

    def visitMultiplicativeExpr(self, ctx):
        assert ctx.myop is not None
        ltype = self.visit(ctx.expr(0))
        rtype = self.visit(ctx.expr(1))
        if ltype == rtype == BaseType.Integer:
            return BaseType.Integer
        elif ctx.myop.type != MiniCParser.MOD and ltype == rtype == BaseType.Float:
            return BaseType.Float
        self._raise(ctx, 'multiplicative operands', ltype, rtype)

    def visitNotExpr(self, ctx):
        etype = self.visit(ctx.expr())
        if etype == BaseType.Boolean:
            return BaseType.Boolean
        self._raise(ctx, 'not operand', etype)

    def visitUnaryMinusExpr(self, ctx):
        etype = self.visit(ctx.expr())
        if etype == BaseType.Integer or etype == BaseType.Float:
            return etype
        self._raise(ctx, 'unary minus operand', etype)

    # visit statements

    def visitPrintlnintStat(self, ctx):
        etype = self.visit(ctx.expr())
        if etype != BaseType.Integer:
            self._raise(ctx, 'println_int statement', etype)

    def visitPrintlnfloatStat(self, ctx):
        etype = self.visit(ctx.expr())
        if etype != BaseType.Float:
            self._raise(ctx, 'println_float statement', etype)

    def visitPrintlnboolStat(self, ctx):
        etype = self.visit(ctx.expr())
        if etype != BaseType.Boolean:
            self._raise(ctx, 'println_bool statement', etype)

    def visitPrintlnstringStat(self, ctx):
        etype = self.visit(ctx.expr())
        if etype != BaseType.String:
            self._raise(ctx, 'println_string statement', etype)

    def visitAssignStat(self, ctx):
        var = ctx.ID().getText()
        if var not in self._memorytypes:
            self._raiseNonType(ctx, "Undefined variable {}".format(var))
        vtype = self._memorytypes[var]
        etype = self.visit(ctx.expr())
        self._assertSameType(ctx, "{}".format(var), vtype, etype)

    def visitWhileStat(self, ctx):
        etype = self.visit(ctx.expr())
        if etype != BaseType.Boolean:
            self._raise(ctx, 'while statement', etype)
        self.visit(ctx.body)

    def visitIfStat(self, ctx):
        etype = self.visit(ctx.expr())
        if etype != BaseType.Boolean:
            self._raise(ctx, 'if statement', etype)
        self.visit(ctx.then_block)
        if ctx.else_block is not None:
            self.visit(ctx.else_block)

    def visitForStat(self, ctx):
        if ctx.init is not None:
            self.visit(ctx.init)
        if ctx.cond is not None:
            etype = self.visit(ctx.cond)
            if etype != BaseType.Boolean:
                self._raise(ctx, 'for statement', etype)
        if ctx.inc is not None:
            self.visit(ctx.inc)
        self.visit(ctx.body)
