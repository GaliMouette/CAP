from typing import List, Dict
from Lib.Errors import MiniCInternalError
from Lib.Operands import Temporary, Operand, S, Offset, DataLocation, GP_REGS
from Lib.Statement import Instruction
from Lib.Allocator import Allocator
from Lib.FunctionData import FunctionData
from Lib import RiscV
from Lib.Graphes import Graph  # For Graph coloring utility functions


class SmartAllocator(Allocator):

    _igraph: Graph  # interference graph

    def __init__(self, fdata: FunctionData, basename: str, liveness,
                 debug=False, debug_graphs=False):
        self._liveness = liveness
        self._basename: str = basename
        self._debug: bool = debug
        self._debug_graphs: bool = debug_graphs
        super().__init__(fdata)

    def replace(self, old_instr: Instruction) -> List[Instruction]:
        """
        Replace Temporary operands with the corresponding allocated
        physical register (Register) OR memory location (Offset).
        """
        before: List[Instruction] = []
        after: List[Instruction] = []
        subst: Dict[Operand, Operand] = {}

        for i, arg in enumerate(old_instr.args(),start=1):
            if isinstance(arg, Temporary):
                loc = arg.get_alloced_loc()
                if isinstance(loc, Offset):
                    if arg in old_instr.used():
                        before.append(RiscV.ld(S[i], loc))
                    if arg in old_instr.defined():
                        after.append(RiscV.sd(S[i], loc))
                    loc = S[i]
                subst[arg] = loc

        # And now return the new list!
        instr = old_instr.substitute(subst)
        return before + [instr] + after

    def prepare(self) -> None:
        """
        Perform all preparatory steps related to smart register allocation:

        - Dataflow analysis to compute the liveness range of each
          temporary.
        - Interference graph construction.
        - Graph coloring.
        - Associating temporaries with actual locations.
        """
        # Liveness analysis
        self._liveness.run()
        # Interference graph
        self.build_interference_graph()
        if self._debug_graphs:
            print("Printing the interference graph")
            self._igraph.print_dot(self._basename + "interference.dot")
        # Smart Allocation via graph coloring
        self.smart_alloc()

    def build_interference_graph(self) -> None:
        """
        Build the interference graph (in self._igraph).
        Vertices of the graph are temporaries,
        and an edge exists between temporaries iff they are in conflict.
        """
        self._igraph: Graph = Graph()
        # Create a vertex for every temporary
        # There may be temporaries the code does not use anymore,
        # but it does not matter as they interfere with no one.
        for v in self._fdata._pool.get_all_temps():
            self._igraph.add_vertex(v)
        # Iterate over self._liveness._liveout (dictionary containing all
        # live out temporaries for each instruction), and for each conflict use
        # self._igraph.add_edge((t1, t2)) to add the corresponding edge.
        for (block, instr), temps in self._liveness._liveout.items():
            if len(temps) > 1:
                for t1 in temps:
                    for t2 in temps:
                        if t1 != t2:
                            self._igraph.add_edge((t1, t2))

    def smart_alloc(self) -> None:
        """
        Allocates all temporaries via graph coloring.
        Prints the colored graph if self._debug_graphs is True.

        Precondition: the interference graph _igraph must have been built.
        """
        # Checking the interference graph has been built
        if not self._igraph:
            raise MiniCInternalError("Empty interference graph in the Smart Allocator")
        # Coloring of the interference graph
        coloringreg: Dict[Temporary, int] = self._igraph.color()
        if self._debug_graphs:
            print("coloring = " + str(coloringreg))
            self._igraph.print_dot(self._basename + "_colored.dot", coloringreg)
        # Temporary -> DataLocation (Register or Offset) dictionary,
        # specifying where a given Temporary should be allocated:
        alloc_dict: Dict[Temporary, DataLocation] = dict()
        # Use the coloring `coloringreg` to fill `alloc_dict`.
        # Our version is less than 5 lines of code.
        for temp in self._fdata._pool.get_all_temps():
            color = coloringreg[temp]
            alloc_dict[temp] = GP_REGS[color] if color in GP_REGS else self._fdata.fresh_offset()
        if self._debug:
            print("Allocation:")
            print(alloc_dict)
        self._fdata._pool.set_temp_allocation(alloc_dict)
