# SmallPythonCalculator

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A small, arithmetic interpreter written in Python.

---

## Demo

<!-- Replace this placeholder with a short demo GIF showing the REPL or test runs -->
![Demo placeholder](https://via.placeholder.com/800x300.png?text=Calculator+Demo+Placeholder)

---

## Quick start

Install and run from the repository root:

1. Run the calculator
    ```bash
    python src/main.py
    ```

2. At the prompt, type expressions and press Enter:
    ```
    ? - 2 + 3 * (4 - 1)
    11
    ? - 10 / 2 + 5
    10
    ? - 5 / 0
    You cannot divide by zero
    ```

Notes:
- This is an integer-only calculator. Decimal numbers are currently unsupported.
- Division truncates toward zero (integer division behavior). So `5 / 3 = 1`, and` -5 / 3 = -1`.

---

## Features

- Addition (+), subtraction (-), multiplication (*), division (/)
- Parentheses and nested grouping
- Operator precedence (multiplication/division before addition/subtraction)
- Clear error message for division by zero

---

## Grammar

The parser follows this BNF-style grammar:

```
<expression> : <expression> '+' <term>
             | <expression> '-' <term>
             | <term>

<term>       : <term> '*' <factor>
             | <term> '/' <factor>
             | <factor>

<factor>     : '-' <factor>
             | '+' <factor>
             | <primary>

<primary>    : NUMBER
             | '(' <expression> ')'
```

(full grammar in `calculator_grammar.bnf`)

---

## Examples

- Basic arithmetic:
  - `2 + 2` → `4`
  - `7 - 10` → `-3`

- Precedence and grouping:
  - `2 + 3 * 4` → `14`
  - `(2 + 3) * 4` → `20`

- Unary operators:
  - `-5` → `-5`
  - `--5` → `5`
  - `3 + -2` → `1`

- Integer division:
  - `8 / 3` → `2`  (truncated)

---

## License

This project is licensed under the MIT License — see `LICENSE`.
