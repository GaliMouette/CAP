# MiniC Compiler
LAB4 (simple code generation), MIF08 / CAP 2022-23

# Authors

Alexis CARRÉ

# Contents

For my extension I decided to implement code generation for the C-for loops
Sadly I could not find caused them to malfunction in the previous lab (lab3)

# Test design

Tests in `exprs` try as many cases as possible for boolean and arithmetic expressions
Tests in `control` are for branching, loops, ...
I didn't do any particular cases for tests on allocation because I don't see what I could add. All the things I could think of are already tested.

# Design choices

I used `1 - b` to implement the boolean not because it is simple and there is no single instruction to do it.

For the all-in-mem allocation, I went for the simplest allocation as possible.
An instruction takes 3 parameters or fewer. So I just use them in order.
The first parameter goes in S[1], the second in S[2] and the third in S[3]

# Known bugs

None for now

# Checklists

A check ([X]) means that the feature is implemented
and *tested* with appropriate test cases.

## Code generation

- [X] Number Atom
- [X] Boolean Atom
- [X] Id Atom
- [X] Additive expression
- [X] Multiplicative expression
- [X] UnaryMinus expression
- [X] Or expression
- [X] And expression
- [X] Equality expression
- [X] Relational expression (! many cases -> many tests)
- [X] Not expression

## Statements

- [X] Prog, assignements
- [X] While
- [X] Cond Block
- [X] If
- [X] Nested ifs
- [X] Nested whiles

## Allocation

- [X] Naive allocation
- [X] All in memory allocation
- [X] Massive tests of memory allocation
