# CyberSec-Lab

Repository containing lab exercises and practical activities from the Master's Degree course in Computer Security at UNIMORE.

## Project Overview

This repository collects practical exercises focused on exploiting typical web and system vulnerabilities including:

- Buffer Overflow in C programs
- SQL Injection on web applications (OWASP Mutillidae II)
- Cross-Site Scripting (XSS)

Each lab includes source code, detailed documentation, and step-by-step exploitation processes to deepen understanding of system internals and web application security.

---

## Repository Structure

CyberSec-Lab/
├── BufferOverflow/              # Buffer overflow lab
│   ├── docs/                    # Markdown documentation and assets
│   └── src/                     # Source code in C
├── SQLInjection/                # SQL Injection lab (OWASP Mutillidae II)
│   ├── docs/                    # Markdown + PDF documentation
│   └── src/                     # Python scripts for SQLi Blind automation
├── XSS/                         # Cross-Site Scripting lab
│   ├── doc/                     # Exercises and screenshots
│   └── src/                     # (TBD)
└── README.md                    # Main repository description

---

## Buffer Overflow

This section includes C programs that demonstrate memory corruption via buffer overflow, along with full analysis using GDB.

### Exercises

1. [Exercise 1](BufferOverflow/docs/exercise1.md) – Basic buffer overflow and stack layout
2. [Exercise 2](BufferOverflow/docs/exercise2.md) – Variable modification via buffer overflow
3. [Exercise 2.1](BufferOverflow/docs/exercise2_1.md) – Variant of Exercise 2
4. [Exercise 3](BufferOverflow/docs/exercise3.md) – Function pointer overflow
5. [Exercise 3.1](BufferOverflow/docs/exercise3_1.md) – Return address modification

---

## SQL Injection

This section focuses on exploiting SQL Injection vulnerabilities using OWASP Mutillidae II, a deliberately vulnerable web application.

### Features

- Authentication bypass
- UNION-based injection
- Information schema enumeration
- File reading via `LOAD_FILE`
- Blind SQL Injection
- Python script to automate blind password extraction

### Documentation

- [SQL Injection Exercises](SQLInjection/docs/exercises.md)
- [Script](SQLInjection/src/blind_bruteforce.py) – Python automation of blind SQLi using `SUBSTRING` and `LIMIT OFFSET`

---

## XSS (Cross-Site Scripting)

This section explores XSS vulnerabilities and payload crafting techniques.

### Exercises

- [Exercise 1](XSS/doc/es1.md) – Basic reflected XSS
- [Exercise 2](XSS/doc/es2.md) – Stored XSS and HTML injection

---

## Requirements

- Python 3.x (for automation scripts)
- Requests library: `pip install requests`
- VirtualBox + Mutillidae VM (provided by the course)
- GDB (for buffer overflow debugging)

---

## Credits

Master's Degree in Computer Science – Security Course  
University of Modena and Reggio Emilia – A.Y. 2024/2025  
Exercises conducted using OWASP Mutillidae II, gcc, gdb, and Python.
