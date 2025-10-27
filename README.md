# SmallPythonCalculator
A small arithmetic interpreter written in Python

## Example Usage
- Run `src/main.py` to start the calculator.


- Enter arithmetic expressions to evaluate them:
```
>>> 2 + 3 * (4 - 1)
11
>>> 10 / 2 + 5
10
>>>  5 / 0
You cannot divide by zero
```

- Decimal numbers are NOT supported:
```
>>> 5.0
Found an invalid character: '.'
```

## Supported Operations
- Addition (`+`)
- Subtraction (`-`)
- Multiplication (`*`)
- Division (`/`)
- Parentheses for grouping (`(` and `)`)
- Positive or negative integers

## Grammar
The grammar used to create this interpreter can be found [here](calculator_grammar.bnf)
