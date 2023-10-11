# MiniC Compiler
LAB5 (smart code generation), MIF08 / CAP 2022-23

# Authors

YOUR NAME HERE

# Contents

TODO for STUDENTS : Say a bit about the code infrastructure ...

# Howto

To compile and run a program:
```
$ python3 ./MiniCC.py --reg-alloc=smart TP04/tests/provided/step1/test00.c
Code will be generated in file TP04/tests/provided/step1/test00.s
$ riscv64-unknown-elf-gcc TP04/tests/provided/step1/test00.s ../TP01/riscv/libprint.s -o /tmp/a.out
$ spike pk /tmp/a.out
```

To launch the testsuite:
```
make test-smart
```

# Test design

TODO: explain your tests

# Design choices

TODO: explain your choices

# Known bugs

TODO: Bugs and limitations.

