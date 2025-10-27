from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Union
from enum import Enum

# token type constants (shared)
NUMBER_TOKEN_TYPE = "NUMBER"
PLUS_TOKEN_TYPE = "PLUS"
MINUS_TOKEN_TYPE = "MINUS"
MULTIPLY_TOKEN_TYPE = "MULTIPLY"
DIVIDE_TOKEN_TYPE = "DIVIDE"
WHITESPACE_TOKEN_TYPE = "WHITESPACE"
LPAREN_TOKEN_TYPE = "LPAREN"
RPAREN_TOKEN_TYPE = "RPAREN"

TokenType = str


@dataclass
class Token:
    """
    Represents a lexical token with its type and value.
    """

    token_type: TokenType
    token_value: str = ""


@dataclass
class LexerResult:
    """
    Represents the result of the lexical analysis (lexing) process.

    - error_message will always be an empty string if was_successful is True.
    """

    was_successful: bool
    tokens: List[Token] = field(default_factory=list)
    error_message: str = ""


@dataclass
class FactorNode:
    """
    Represents a factor in an arithmetic expression, which can be a number or a nested expression.

    Note that number is stored as a string opposed to an integer. It will be converted to an integer during interpretation.
    """

    sign: int = 1  # 1 for positive, -1 for negative
    number: Optional[str] = None
    nested_expression: Optional[ExpressionNode] = None


# allow nesting so we can build left-associative trees
@dataclass
class TermNode:
    """
    Represents a term in an arithmetic expression, which can consist of factors combined by multiplication or division.
    """

    first_factor_node: FactorNode | TermNode
    operator: Optional[ArithmeticOperator] = None
    second_factor_node: Optional[FactorNode] = None


@dataclass
class ExpressionNode:
    """
    Represents an arithmetic expression, which can consist of terms combined by addition or subtraction.
    """

    single_term_node: TermNode | ExpressionNode
    operator: Optional[ArithmeticOperator] = None
    additional_expression_node: Optional[ExpressionNode] = None


class ArithmeticOperator(Enum):
    """
    Represents arithmetic operators for expressions.
    """

    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
