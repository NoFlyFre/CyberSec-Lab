# CyberSec-Lab

Repository containing lab exercises and practical activities from the Master's Degree course in Computer Security at UNIMORE.

## Project Overview

This repository contains practical exercises focused on exploiting buffer overflow vulnerabilities in C programs. The exercises demonstrate fundamental security concepts including:

- Stack memory organization and manipulation
- Variable overwriting through buffer overflow
- Execution flow hijacking
- Function pointer manipulation
- Return address modification

Each exercise includes source code, detailed explanation, and step-by-step analysis using GDB to understand the underlying memory manipulation.

## Repository Structure

```
CyberSec-Lab/
└── BufferOverflow/              # Buffer overflow exercise directory
    ├── docs/                    # Documentation for each exercise
    │   ├── exercise1.md         # Buffer overflow basics and stack analysis
    │   ├── exercise2.md         # Variable modification via overflow
    │   ├── exercise2_1.md       # Variable modification variant
    │   ├── exercise3.md         # Function pointer overflow
    │   └── exercise3_1.md       # Return address modification
    └── src/                     # Source code for all exercises
        ├── esercizio1.c         # Basic buffer overflow example
        ├── esercizio2.c         # Variable modification example
        ├── esercizio2_1.c       # Variable modification variant
        ├── esercizio3.c         # Function pointer overflow example
        └── esercizio3_1.c       # Return address modification example
```

## Exercise Documentation

Each buffer overflow exercise is documented separately:

1. [Exercise 1](BufferOverflow/docs/exercise1.md) - Basic buffer overflow and stack analysis
2. [Exercise 2](BufferOverflow/docs/exercise2.md) - Variable modification via buffer overflow
3. [Exercise 2.1](BufferOverflow/docs/exercise2_1.md) - Variable modification variant
4. [Exercise 3](BufferOverflow/docs/exercise3.md) - Function pointer overflow
5. [Exercise 3.1](BufferOverflow/docs/exercise3_1.md) - Return address modification