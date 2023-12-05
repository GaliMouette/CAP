# Planning of the compilation course (CAP, Compilation and Program Analysis)
_Academic first semester 2023-2024_

# Week 1:

- :book: Course: Tuesday 12/09/2023, 13h30-15h30. Amphi B (Gabriel Radanne)
  
  * Introduction: [transparents](course/capmif_cours01_intro_et_archi.pdf).
  * ISA [ref pdf RISCV](course/riscv_isa.pdf).
  * [Demo Assembly](course/demo20.s).
  * Lexing, Parsing, [slides](course/capmif_cours02_lexing_parsing.pdf).
  * [Demo Parsing](course/ANTLRExamples.tar.xz).

- :hammer: Lab 1: Thursday 14/09/2023, 8h00-10h00. Room E001 (Samuel Humeau & Hugo Thievenaz)

  * Introduction to RISCV [TP01](TP01/tp1.pdf).
  * Code in [TP01/](TP01/).
  * ISA [ref pdf RISCV](course/riscv_isa.pdf).

- :rocket: Additional ressources (mainly in english)

  * A nice YT video on [structural induction](https://www.youtube.com/watch?v=2o3EzvfgTiQ) by F. Pereira.
  * Fernando Pereira's other videos on operational semantics : [video1](https://www.youtube.com/watch?v=bOzbRhXvtlY), [video2](https://www.youtube.com/watch?v=aiBKOuM5iEA).

# Week 2:

- :book: Course: Tuesday 19/09/2023, 13h30-15h30. Amphi B (Ludovic Henrio)

  * Semantics [slides in english](course/CAP_Semantics.pdf).

- :book: Course: Thursday 21/09/2023, 8h00-10h00. **Amphi B** (Ludovic Henrio)

  * Typing [slides in english](course/CAP_cours04_typing.pdf).

# Week 3:

- :book: Course: Tuesday 26/09/2023, 13h30-15h30. Amphi B (Gabriel Radanne)

  * Interpreters [slides in english](course/capmif_cours03_interpreters.pdf).
  * [Demo files](course/ANTLRExamples.tar.xz).
  * [Grammar exercise](course/TD2.pdf).

- :hammer: Lab 2: Thursday 28/09/2023, 8h00-10h00. Room E001 (Samuel Humeau & Hugo Thievenaz)

  * Lexing & Parsing with ANTLR4 [TP02](TP02/tp2.pdf).
  * Code in [TP02/](TP02/).

# Week 4:

- :book: Course: Monday 03/10/2023, 13h30-15h30. Amphi B (Gabriel Radanne)

  * 3A Code Generation [slides in english](course/capmif_cours05_3ad_codegen.pdf).
  * CFG (first section) [slides in english](course/capmif_cours06_irs.pdf).

- :hammer: Lab 3: Thursday 05/10/2023, 8h00-10h00. Room E001 (Samuel Humeau & Hugo Thievenaz)

  * Interpreter & Typer [TP03](TP03/tp3.pdf).
  * Code in [TP03/](TP03/) and [MiniC/TP03/](MiniC/TP03/).

# Week 5:

- :hammer: Lab 4a: Thursday 12/10/2023, 8h00-10h00. Room E001 (Samuel Humeau & Hugo Thievenaz)

  * Syntax directed code generation [TP04](TP04/tp4a.pdf).
  * Code in [MiniC/TP04/](MiniC/TP04/).
  * Documentation [here](docs/html/index.html).

# Week 6:

- :book: Course: Monday 17/10/2023, 13h30-15h30. Amphi B (Gabriel Radanne)

  * CFG (second section) [slides in english](course/capmif_cours06_irs.pdf).

- :hammer: Lab 4b: Thursday 19/10/2023, 8h00-10h00. Room E001 (Samuel Humeau & Hugo Thievenaz)

  * Control Flow Graph [TP04b](TP04/tp4b.pdf).
  * Code in [MiniC/TP04/](MiniC/TP04/).
  * Documentation (updated) [here](docs/html/index.html).

# Week 7:

- :book: Course: Monday 24/10/2023, 13h30-15h30. Amphi B (Gabriel Radanne)

  * Register allocation [slides in english](course/cap_cours07_regalloc.pdf)

- :hammer: Lab 5a: Thursday 26/10/2023, 8h00-10h00. Room E001 (Samuel Humeau & Hugo Thievenaz)

  * Control Flow Graph under SSA Form [TP05a](TP05/tp5a.pdf).
  * Code in [MiniC/TP05/](MiniC/TP05/).
  * Documentation (updated) [here](docs/html/index.html).

# Week 8:

- :hammer: Lab 5b (1/2): Thursday 09/11/2023, 8h00-10h00. Room E001 (Samuel Humeau & Hugo Thievenaz)

    * Smart Register Allocation [TP05b](TP05/tp5b.pdf).
    * Code in [MiniC/TP05/](MiniC/TP05/).

# Week 9:

- :book: Course: Tuesday 14/11/2023, 13h30-15h30. Amphi B (Ludovic Henrio)

  * Functions: Code generation and typing [slides in english](course/cap_cours09A_func_codegen_typing.pdf)

- :hammer: Lab 5b (2/2): Thursday 16/11/2021, 8h00-10h00. Rooms E001 (Samuel Humeau & Hugo Thievenaz)

# Week 10:

- :book: Course: Tuesday 21/11/2023, 13h30-15h30. Amphi B (Ludovic Henrio)

  * Functions: semantics [slides in english](course/cap_cours09B_funsem.pdf)


- :notebook: TD: Thursday 23/11/2021, 8h00-10h00. Rooms E001 (Samuel Humeau & Hugo Thievenaz)


# Week 11:

- :book: Course: Tuesday 28/11/2023, 13h30-15h30. ROOM 435S (4th floor, south building) (Ludovic Henrio)

  * Parallelism 1 : Futures [slides in english](course/cap_cours11_parallelism.pdf)


- :hammer: Choice Lab (1/3): Thursday 30/11/2021, 8h00-10h00. Rooms E001 (Samuel Humeau & Hugo Thievenaz)

    * Optimisations under SSA form [TP5c](TP05/tp5c.pdf), code in [MiniC/TPoptim/](MiniC/TPoptim/).
    * Parsing and typechecking functions [TP06a](TP06/tp6a.pdf), code in [MiniC/](MiniC/).
    * Going Parallel with futures [TPfutures](TPfutures/tpfutures.pdf), code in [TPfutures/MiniC-futures/](TPfutures/MiniC-futures/).
    * Code generation for functions [TP06b](TP06/tp6b.pdf), code in [MiniC/](MiniC/).  
  
  
  # Week 12:

- :book: Course: Tuesday 5/12/2023, 13h30-15h30. Amphi B (Ludovic Henrio)

 * Parallelism 2 : Semantics, implementing languages, and advanced futures [slides in english](course/cap_cours13_parallelismAdvanced.pdf)
 

