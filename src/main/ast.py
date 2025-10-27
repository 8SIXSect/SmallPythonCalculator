from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Union, AnyStr
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
    token_type: TokenType
    token_value: str = ""

@dataclass
class LexerResult:
    was_successful: bool
    tokens: List[Token] = field(default_factory=list)
    error_message: str = ""

@dataclass
class InterpreterResult:
    was_successful: bool
    output: int = 0
    error_message: str = ""

@dataclass
class ParserResult:
    was_successful: bool
    syntax_tree: Optional["ExpressionNode"] = None
    error_message: str = ""

@dataclass
class NodeResult:
    was_successful: bool
    tokens: Optional[List[Token]] = field(default_factory=list)
    node: Optional[Union["ExpressionNode", "TermNode", "FactorNode"]] = None
    error_message: str = ""

@dataclass
class FactorNode:
    sign: int = 1
    number: Optional[str] = None
    nested_expression: Optional["ExpressionNode"] = None

# allow nesting so we can build left-associative trees
@dataclass
class TermNode:
    first_factor_node: Union[FactorNode, "TermNode"]
    operator: Optional["ArithmeticOperator"] = None
    second_factor_node: Optional[FactorNode] = None

@dataclass
class ExpressionNode:
    single_term_node: Union[TermNode, "ExpressionNode"]
    operator: Optional["ArithmeticOperator"] = None
    additional_expression_node: Optional["ExpressionNode"] = None

class ArithmeticOperator(Enum):
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"

