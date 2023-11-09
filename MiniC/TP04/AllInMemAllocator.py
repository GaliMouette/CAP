from Lib import RiscV
from Lib.Operands import Temporary, Operand, S
from Lib.Statement import Instruction
from Lib.Allocator import Allocator
from typing import List, Dict


class AllInMemAllocator(Allocator):

    def replace(self, old_instr: Instruction) -> List[Instruction]:
        """Replace Temporary operands with the corresponding allocated
        memory location."""
        before: List[Instruction] = []
        after: List[Instruction] = []
        subst: Dict[Operand, Operand] = {}
        for i, arg in enumerate(old_instr.args(),start=1):
            if isinstance(arg, Temporary):
                subst[arg] = S[i]
                loc = arg.get_alloced_loc()
                if arg in old_instr.used():
                    before.append(RiscV.ld(S[i], loc))
                if arg in old_instr.defined():
                    after.append(RiscV.sd(S[i], loc))
        new_instr = old_instr.substitute(subst)
        return before + [new_instr] + after

    def prepare(self) -> None:
        """Allocate all temporaries to memory.
        Invariants:
        - Expanded instructions can use s2 and s3
          (to store the values of temporaries before the actual instruction).
        """
        self._fdata._pool.set_temp_allocation(
            {temp: self._fdata.fresh_offset()
             for temp in self._fdata._pool.get_all_temps()})
