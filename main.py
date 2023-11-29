from __future__ import annotations
import re
from typing import List, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum


# todo: convert these strings into an enumeration
NUMBER_TOKEN_TYPE = "NUMBER"
PLUS_TOKEN_TYPE = "PLUS"
MINUS_TOKEN_TYPE = "MINUS"
MULTIPLY_TOKEN_TYPE = "MULTIPLY"
DIVIDE_TOKEN_TYPE = "DIVIDE"
WHITESPACE_TOKEN_TYPE = "WHITESPACE"

token_patterns = {
    r"\d+": NUMBER_TOKEN_TYPE,
    r"\+": PLUS_TOKEN_TYPE,
    r"\-": MINUS_TOKEN_TYPE,
    r"\*": MULTIPLY_TOKEN_TYPE,
    r"/": DIVIDE_TOKEN_TYPE,
    r"\s": WHITESPACE_TOKEN_TYPE,
}


TokenType = str


@dataclass
class Token:
    """ Building block of the lexer """

    token_type: TokenType 
    token_value: Optional[str]



@dataclass
class LexerResult:
    was_successful: bool
    tokens: List[Token] = field(default_factory=list) 
    error_message: str = ""


def scan_and_tokenize_input(user_input: str) -> LexerResult:
    """"""

    def report_error(unknown_character: str) -> LexerResult:
        """"""

        ERROR_MESSAGE = "Found an unknown character, '{0}'"

        error_message: str = ERROR_MESSAGE.format(unknown_character)

        lexer_result = LexerResult(False, error_message=error_message)
        return lexer_result 
    

    tokens: List[Token] = []
    position = 0
    length_of_input: int = len(user_input)
    
    while position < length_of_input:
        match: Union[re.Match[str], None] = None

        # Incase you don't remember hunter, this gives you everything after
        # position
        sliced_input = user_input[position:]
        
        pattern: str

        for pattern in token_patterns.keys():

            match = re.match(pattern,sliced_input)

            if match is not None:

                token_type: TokenType = token_patterns[pattern]
                if token_type == WHITESPACE_TOKEN_TYPE:
                    break

                token_value: str = match.group(0)
                token = Token(token_type, token_value)
                
                tokens.append(token)
                break
        
        if match is None:

            unknown_character = user_input[position]
            unsuccessful_result: LexerResult = report_error(unknown_character)
            
            return unsuccessful_result

        position += match.end()

    was_successful = True
    return LexerResult(was_successful, tokens)


@dataclass
class ParserResult:
    """"""

    was_successful: bool
    syntax_tree: Optional[ExpressionNode] = None
    error_message: str = ""


@dataclass
class NodeResult:
    was_successful: bool
    tokens: Optional[List[Token]] = None
    node: Union[ExpressionNode, TermNode, FactorNode, None] = None
    error_message: str = ""


@dataclass
class ExpressionNode:
    first_term_node: TermNode
    operator: Optional[ArithmeticOperator] = None
    second_term_node: Optional[TermNode] = None


@dataclass
class TermNode:
    first_factor_node: FactorNode
    operator: Optional[ArithmeticOperator] = None
    second_factor_node: Optional[FactorNode] = None


@dataclass
class FactorNode:
    number: str


class ArithmeticOperator(Enum):
    
    # The values of these enum members does not matter
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"


def parse_list_of_tokens(tokens: List[Token]) -> ParserResult:
    """"""

    def report_error(unexpected_token_type: TokenType) -> NodeResult:
        """"""

        ERROR_MESSAGE = "Found an unexpected token, '{0}'"

        error_message: str = ERROR_MESSAGE.format(unexpected_token_type)

        node_result = NodeResult(False, error_message=error_message)
        return node_result


    def parse_tokens_for_expression(tokens: List[Token]) -> NodeResult:

        EXPRESSION_TOKEN_TYPES: Tuple[TokenType, TokenType] = (PLUS_TOKEN_TYPE, MINUS_TOKEN_TYPE)
 
        term_node_result: NodeResult = parse_tokens_for_term(tokens)

        if not term_node_result.was_successful:
            return term_node_result

        first_term_node: TermNode = term_node_result.node
        expression_node = ExpressionNode(first_term_node)

        node_result_for_simple_expression = NodeResult(True, term_node_result.tokens,
                                                       expression_node)

        length_of_tokens = len(node_result_for_simple_expression.tokens)

        if length_of_tokens == 0:
            return node_result_for_simple_expression 

        # We don't pop the token off b/c there's a chance it's not a + or -
        current_token = tokens[0]

        if current_token.token_type not in EXPRESSION_TOKEN_TYPES:
            print(current_token, tokens)
            return node_result_for_simple_expression 

        del tokens[0]

        expression_node_operator: ArithmeticOperator

        if current_token.token_type == PLUS_TOKEN_TYPE:
            expression_node_operator = ArithmeticOperator.PLUS
        else:
            expression_node_operator = ArithmeticOperator.MINUS

        # Variable 'tokens' is reassigned here for clarity. It is not needed above, so that
        # is why it was reassigned down here
        # Also, you don't really have to have this if statement but it makes my linter happy
        if term_node_result.tokens is not None:
            tokens = term_node_result.tokens.copy()

        second_term_node_result: NodeResult = parse_tokens_for_term(tokens)
        
        if not second_term_node_result.was_successful:
            return second_term_node_result

        second_term_node_for_complex_expression_node = second_term_node_result.node

        # Redundant if statement that makes my linter happy
        if second_term_node_result.tokens is not None:
            tokens = second_term_node_result.tokens.copy()

        complex_term_node = ExpressionNode(expression_node.first_term_node,
                                           expression_node_operator,
                                           second_term_node_for_complex_expression_node)

        return NodeResult(True, tokens, complex_term_node)
 

    def parse_tokens_for_term(tokens: List[Token]) -> NodeResult:

        TERM_TOKEN_TYPES: Tuple[TokenType, TokenType] = (MULTIPLY_TOKEN_TYPE,
                                                         DIVIDE_TOKEN_TYPE)
        
        factor_node_result: NodeResult = parse_tokens_for_factor(tokens)

        if not factor_node_result.was_successful:
            return factor_node_result

        first_factor_node: FactorNode = factor_node_result.node
        term_node = TermNode(first_factor_node)

        node_result_for_simple_term = NodeResult(True, factor_node_result.tokens, term_node)

        length_of_tokens = len(node_result_for_simple_term.tokens)

        if length_of_tokens == 0:
            return node_result_for_simple_term 

        # We don't pop the token off b/c there's a chance it's not a * or /
        current_token = tokens[0]
        print("\n\n\n", tokens, factor_node_result.tokens, tokens is factor_node_result.tokens, "\n\n\n")

        if current_token.token_type not in TERM_TOKEN_TYPES:
            return node_result_for_simple_term 

        del tokens[0]

        term_node_operator: ArithmeticOperator

        if current_token.token_type == MULTIPLY_TOKEN_TYPE:
            term_node_operator = ArithmeticOperator.MULTIPLY
        else:
            term_node_operator = ArithmeticOperator.DIVIDE

        # Variable 'tokens' is reassigned here for clarity. It is not needed above, so that
        # is why it was reassigned down here
        # Also, you don't really have to have this if statement but it makes my linter happy
        if factor_node_result.tokens is not None:
            tokens = factor_node_result.tokens.copy()

        second_factor_node_result: NodeResult = parse_tokens_for_factor(tokens)
        
        if not second_factor_node_result.was_successful:
            return second_factor_node_result

        second_factor_node_for_complex_term_node = second_factor_node_result.node

        # Redundant if statement that makes my linter happy
        if second_factor_node_result.tokens is not None:
            tokens = second_factor_node_result.tokens.copy()

        complex_term_node = TermNode(term_node.first_factor_node,
                                     term_node_operator,
                                     second_factor_node_for_complex_term_node)

        return NodeResult(True, tokens, complex_term_node)
            

    def parse_tokens_for_factor(tokens: List[Token]) -> NodeResult:

        current_token = tokens.pop(0)

        if current_token.token_type != NUMBER_TOKEN_TYPE:
            return report_error(current_token.token_type)

        factor_node = FactorNode(current_token.token_value)

        return NodeResult(True, tokens, factor_node)

    r = parse_tokens_for_expression(tokens)
    print(r)


if __name__ == "__main__":
    USER_INPUT = "5/6+1"
    lexer_result: LexerResult = scan_and_tokenize_input(USER_INPUT)
    
    if lexer_result.was_successful:
        parse_list_of_tokens(lexer_result.tokens)

    else:
        print(lexer_result.error_message)

