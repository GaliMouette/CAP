from typing import Dict, Set, Tuple
from Lib.Operands import Temporary
from Lib.Statement import Statement, regset_to_string
from Lib.CFG import Block, CFG
from Lib.PhiNode import PhiNode


class LivenessSSA:
    """Liveness Analysis on a CFG under SSA Form."""

    def __init__(self, cfg: CFG, debug=False):
        self._cfg: CFG = cfg
        self._debug: bool = debug
        # Temporary already propagated, by Block
        self._seen: Dict[Block, Set[Temporary]] = dict()
        # Live Temporary at outputs of Statement
        self._liveout: Dict[tuple[Block, Statement], Set[Temporary]] = dict()

    def run(self) -> None:
        """Compute the liveness: fill out self._seen and self._liveout."""
        # Initialization
        for block in self._cfg.get_blocks():
            self._seen[block] = set()
            for instr in block.get_all_statements():
                self._liveout[block, instr] = set()
        # Start the used-defined chains with backward propagation of liveness information
        for var, uses in self.gather_uses().items():
            for block, pos in uses:
                self.livein_at_instruction(block, pos, var)
        # Add conflicts on phis
        self.conflict_on_phis()
        # Final debugging print
        if self._debug:
            self.print_map_in_out()

    def livein_at_instruction(self, block: Block, pos: int, var: Temporary) -> None:
        """Backward propagation of liveness information at the beginning of an instruction."""
        instr = block.get_all_statements()[pos]
        if isinstance(instr, PhiNode) and var in instr.used():
            for key, item in instr.get_srcs().items():
                if item == var:
                    for pred in block.get_in():
                        if pred.get_label() == key:
                            self.liveout_at_block(pred, var)
        elif pos == 0:
            for pred in block.get_in():
                self.liveout_at_block(pred, var)
        else:
            self.liveout_at_instruction(block, pos - 1, var)

    def liveout_at_instruction(self, block: Block, pos: int, var: Temporary) -> None:
        """Backward propagation of liveness information at the end of an instruction."""
        instr = block.get_all_statements()[pos]
        self._liveout[block, instr].add(var)
        if var not in instr.defined():
            self.livein_at_instruction(block, pos, var)

    def liveout_at_block(self, block: Block, var: Temporary) -> None:
        """Backward propagation of liveness information at the end of a block."""
        if var not in self._seen[block]:
            self._seen[block].add(var)
            self.liveout_at_instruction(block, len(block.get_all_statements()) - 1, var)

    def gather_uses(self) -> Dict[Temporary, Set[Tuple[Block, int]]]:
        """
        Return a dictionnary giving for each variable the set of statements using it,
        with a statement identified by its block and its position inside the latter.
        Phi instructions are at the beginning of their block, while a Terminator is at
        the last position of its block.
        """
        uses: Dict[Temporary, Set[Tuple[Block, int]]] = dict()
        for block in self._cfg.get_blocks():
            for pos, instr in enumerate(block.get_all_statements()):
                # Variables used by a statement `s` are `s.used()`
                for var in instr.used():
                    if isinstance(var, Temporary):
                        # Already computed uses of the var if any, otherwise the empty set
                        var_uses = uses.get(var, set())
                        # Add for a statement its block and its position inside to the uses of var
                        uses[var] = var_uses.union({(block, pos)})
        return uses

    def conflict_on_phis(self) -> None:
        """Ensures that variables defined by φ instructions are in conflict with one-another."""
        blocks = self._cfg.get_blocks()
        for block in blocks:
            for phi in block.get_phis():
                assert isinstance(phi, PhiNode)
                if isinstance(phi.var, Temporary):
                    self.liveout_at_block(block, phi.var)

    def print_map_in_out(self) -> None:  # pragma: no cover
        """Print live out sets at each instruction, group by block, useful for debugging!"""
        print("Liveout: [")
        for block in self._cfg.get_blocks():
            print("Block " + str(block.get_label()) + ": {\n "
                  + ",\n ".join("\"{}\": {}"
                  .format(instr, regset_to_string(self._liveout[block, instr]))
                  for instr in block.get_all_statements()) +
                  "}")
        print("]")
