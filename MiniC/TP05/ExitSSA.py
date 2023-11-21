"""
CAP, SSA Intro, Elimination and Optimisations
Functions to convert a CFG out of SSA Form.
"""

from typing import cast, List
from Lib import RiscV
from Lib.CFG import Block, BlockInstr, CFG
from Lib.Operands import Temporary
from Lib.Statement import AbsoluteJump, Label
from Lib.Terminator import BranchingTerminator, Return
from Lib.PhiNode import PhiNode
from TP05.SequentializeMoves import sequentialize_moves


def generate_moves_from_phis(phis: List[PhiNode], parent: Block) -> List[BlockInstr]:
    """
    `generate_moves_from_phis(phis, parent)` builds a list of move instructions
    to be inserted in a new block between `parent` and the block with phi nodes
    `phis`.

    This is an helper function called during SSA exit.
    """
    moves: List[BlockInstr] = []

    for phi in phis:
        if parent.get_label() in phi.srcs:
            dest = phi.var
            src = phi.srcs[parent.get_label()]
            move = RiscV.mv(dest, src)
            moves.append(move)

    return moves


def exit_ssa(cfg: CFG, is_smart: bool) -> None:
    """
    `exit_ssa(cfg)` replaces phi nodes with move instructions to exit SSA form.

    `is_smart` is set to true when smart register allocation is enabled (Lab 5b).
    """
    for b in cfg.get_blocks():
        phis = cast(List[PhiNode], b.get_phis())  # Use cast for Pyright
        b.remove_all_phis()  # Remove all phi nodes in the block
        parents: List[Block] = b.get_in().copy()  # Copy as we modify it by adding blocks
        for parent in parents:
            moves = generate_moves_from_phis(phis, parent)
            label = Label("phi_{}_{}".format(b.get_label(), parent.get_label()))
            jump = AbsoluteJump(b.get_label())
            block = Block(label, moves, jump)
            cfg.add_block(block)
            match parent.get_terminator():
                case AbsoluteJump():
                    parent.set_terminator(AbsoluteJump(label))
                case BranchingTerminator() as bt:
                    if b.get_label() == bt.label_then:
                        bt.label_then = label
                    elif b.get_label() == bt.label_else:
                        bt.label_else = label
                    else:
                        raise Exception("exit_ssa: Unknown label")
            cfg.remove_edge(parent, b)
            cfg.add_edge(parent, block)
            cfg.add_edge(block, b)
