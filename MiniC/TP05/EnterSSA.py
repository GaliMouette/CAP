"""
CAP, SSA Intro, Elimination and Optimisations
Functions to convert a CFG into SSA Form.
"""

from typing import List, Dict, Set
from Lib.CFG import Block, CFG
from Lib.Operands import Renamer
from Lib.Statement import Instruction
from Lib.PhiNode import PhiNode
from Lib.Dominators import computeDom, computeDT, computeDF


def insertPhis(cfg: CFG, DF: Dict[Block, Set[Block]]) -> None:
    """
    `insertPhis(CFG, DF)` inserts phi nodes in `cfg` where needed.
    At this point, phi nodes will look like `temp_x = φ(temp_x, ..., temp_x)`.

    This is an helper function called during SSA entry.
    """
    for var, defs in cfg.gather_defs().items():
        has_phi: Set[Block] = set()
        queue: List[Block] = list(defs)
        while queue:
            d = queue.pop(0)
            for b in DF[d]:
                if b not in has_phi:
                    assert len(b.get_in()) > 1
                    phi = PhiNode(var, {e.get_label(): var for e in b.get_in()})
                    b.add_phi(phi)
                    has_phi.add(b)
                    queue.append(b)


def rename_block(cfg: CFG, DT: Dict[Block, Set[Block]], renamer: Renamer, b: Block) -> None:
    """
    Rename variables from block b.

    This is an auxiliary function for `rename_variables`.
    """
    renamer = renamer.copy()
    for i in b.get_all_statements():
        if isinstance(i, Instruction | PhiNode):
            i.rename(renamer)
    for succ in cfg.out_blocks(b):
        for i in succ.get_phis():
            assert (isinstance(i, PhiNode))
            i.rename_from(renamer, b.get_label())
    for dom_by_b in DT[b]:
        rename_block(cfg, DT, renamer, dom_by_b)



def rename_variables(cfg: CFG, DT: Dict[Block, Set[Block]]) -> None:
    """
    Rename variables in the CFG, to transform `temp_x = φ(temp_x, ..., temp_x)`
    into `temp_x = φ(temp_0, ... temp_n)`.

    This is an helper function called during SSA entry.
    """
    renamer = Renamer(cfg.fdata._pool)
    for entry in cfg.get_entries():
        rename_block(cfg, DT, renamer, entry)


def enter_ssa(cfg: CFG, dom_graphs=False, basename="prog") -> None:
    """
    Convert the CFG `cfg` into SSA Form:
    compute the dominance frontier, then insert phi nodes and finally
    rename variables accordingly.

    `dom_graphs` indicates if we have to print the domination graphs.
    `basename` is used for the names of the produced graphs.
    """
    dom = computeDom(cfg)
    dt = computeDT(cfg, dom, dom_graphs, basename)
    df = computeDF(cfg, dom, dt, dom_graphs, basename)

    insertPhis(cfg, df)

    rename_variables(cfg, dt)
