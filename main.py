from __future__ import annotations
import re
from typing import List, Optional, Tuple, Union, AnyStr 
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
    token_value: str = ""



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
    single_term_node: TermNode
    operator: Optional[ArithmeticOperator] = None
    additional_expression_node: Optional[ExpressionNode] = None


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

    class ParserErrorReason:
        UNEXPECTED_TOKEN_TYPE = "Unexpected Token Type, {0}"
        VALUE_IS_NULL = "Found A Null Value; {0} is Null"
        UNEXPECTED_TYPE = "Unexpected Node of Type, {0}"


    def report_error(unexpected_token_type: Optional[TokenType] = None,
                     unexpected_null: Optional[AnyStr] = None,
                     unexpected_type: Optional[AnyStr] = None) -> NodeResult:
        """"""

        error_message = ""

        if unexpected_token_type is not None:
            error_message: str = ParserErrorReason.UNEXPECTED_TOKEN_TYPE.format(
                    unexpected_token_type)
        
        if unexpected_null is not None:
            error_message: str = ParserErrorReason.VALUE_IS_NULL.format(unexpected_null)

        if unexpected_type is not None:
            error_message: str = ParserErrorReason.UNEXPECTED_TYPE.format(unexpected_type)

        node_result = NodeResult(False, error_message=error_message)
        return node_result


    def parse_tokens_for_expression(tokens: List[Token]) -> NodeResult:

        EXPRESSION_TOKEN_TYPES: Tuple[TokenType, TokenType] = (PLUS_TOKEN_TYPE, MINUS_TOKEN_TYPE)
 
        term_node_result: NodeResult = parse_tokens_for_term(tokens)

        if not term_node_result.was_successful:
            return term_node_result

        if not isinstance(term_node_result.node, TermNode):

            type_of_term_node = type(term_node_result.node)
            UNEXPECTED_TYPE = str(type_of_term_node)

            unsuccessful_result: NodeResult = report_error(unexpected_type=UNEXPECTED_TYPE)
            return unsuccessful_result

        first_term_node: TermNode = term_node_result.node
        expression_node = ExpressionNode(first_term_node)

        node_result_for_simple_expression = NodeResult(True, term_node_result.tokens,
                                                       expression_node)
        
        if node_result_for_simple_expression.tokens is None:
            FOUND_NULL_VALUE = "Node Result for Simple Expression is None"            

            unsuccessful_result: NodeResult = report_error(unexpected_null=FOUND_NULL_VALUE)
            return unsuccessful_result

        length_of_tokens = len(node_result_for_simple_expression.tokens)

        if length_of_tokens == 0:
            return node_result_for_simple_expression 

        # We don't pop the token off b/c there's a chance it's not a + or -
        current_token = tokens[0]

        if current_token.token_type not in EXPRESSION_TOKEN_TYPES:
            return node_result_for_simple_expression 

        del tokens[0]

        expression_node_operator: ArithmeticOperator

        if current_token.token_type == PLUS_TOKEN_TYPE:
            expression_node_operator = ArithmeticOperator.PLUS
        else:
            expression_node_operator = ArithmeticOperator.MINUS
       
        if term_node_result.tokens is None:
            FOUND_NULL_VALUE = "Term Node Result Tokens is None"

            unsuccessful_result: NodeResult = report_error(unexpected_null=FOUND_NULL_VALUE)
            return unsuccessful_result

        tokens = term_node_result.tokens 

        additional_expression_node_result: NodeResult = parse_tokens_for_expression(tokens)
        
        if not additional_expression_node_result.was_successful:
            return additional_expression_node_result

        if additional_expression_node_result.tokens is None:
            FOUND_NULL_VALUE = "Additional Expression Node Result is None"

            unsuccessful_result: NodeResult = report_error(unexpected_null=FOUND_NULL_VALUE)
            return unsuccessful_result

        tokens = additional_expression_node_result.tokens

        additional_expression_node = additional_expression_node_result.node

        if not isinstance(additional_expression_node, ExpressionNode):
            type_of_additional_expression_node = type(additional_expression_node)
            UNEXPECTED_TYPE = str(type_of_additional_expression_node)

            unsuccessful_result: NodeResult = report_error(unexpected_type=UNEXPECTED_TYPE)
            return unsuccessful_result

        complex_term_node = ExpressionNode(expression_node.single_term_node,
                                           expression_node_operator,
                                           additional_expression_node)

        return NodeResult(True, tokens, complex_term_node)
 

    def parse_tokens_for_term(tokens: List[Token]) -> NodeResult:
        TERM_TOKEN_TYPES: Tuple[TokenType, TokenType] = (MULTIPLY_TOKEN_TYPE,
                                                         DIVIDE_TOKEN_TYPE)

        factor_node_result: NodeResult = parse_tokens_for_factor(tokens)

        if not factor_node_result.was_successful:
            return factor_node_result

        if not isinstance(factor_node_result.node, FactorNode):
            type_of_factor_node_result_node = type(factor_node_result.node)
            UNEXPECTED_TYPE = str(type_of_factor_node_result_node)

            unsuccessful_result: NodeResult = report_error(unexpected_type=UNEXPECTED_TYPE)
            return unsuccessful_result

        first_factor_node: FactorNode = factor_node_result.node
        term_node = TermNode(first_factor_node)

        node_result_for_simple_term = NodeResult(True, factor_node_result.tokens, term_node)

        if node_result_for_simple_term.tokens is None:
            FOUND_NULL_VALUE = "Node Result for Simple Term's Tokens"
            unsuccessful_result: NodeResult = report_error(unexpected_null=FOUND_NULL_VALUE)
            return unsuccessful_result

        length_of_tokens: int = len(node_result_for_simple_term.tokens)

        if length_of_tokens == 0:
            return node_result_for_simple_term 

        # We don't pop the token off b/c there's a chance it's not a * or /
        current_token = tokens[0]

        if current_token.token_type not in TERM_TOKEN_TYPES:
            return node_result_for_simple_term 

        del tokens[0]

        term_node_operator: ArithmeticOperator

        if current_token.token_type == MULTIPLY_TOKEN_TYPE:
            term_node_operator = ArithmeticOperator.MULTIPLY
        else:
            term_node_operator = ArithmeticOperator.DIVIDE

        if factor_node_result.tokens is not None:
            tokens = factor_node_result.tokens

        second_factor_node_result: NodeResult = parse_tokens_for_factor(tokens)
        
        if not second_factor_node_result.was_successful:
            return second_factor_node_result

        second_factor_node_for_complex_term_node = second_factor_node_result.node

        if second_factor_node_result.tokens is None:
            unsuccessful_result: NodeResult = report_error("Null Error")
            return unsuccessful_result

        tokens = second_factor_node_result.tokens

        if not isinstance(second_factor_node_for_complex_term_node, FactorNode):
            unsuccessful_result: NodeResult = report_error("nil")
            return unsuccessful_result

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


    root_node_result: NodeResult = parse_tokens_for_expression(tokens)

    if not root_node_result.was_successful:
        return ParserResult(False, error_message=root_node_result.error_message)

    if not isinstance(root_node_result.node, ExpressionNode):

        unsuccessful_result: NodeResult = report_error(str(root_node_result.node))
        return ParserResult(False, error_message=unsuccessful_result.error_message)

    root_node: ExpressionNode = root_node_result.node
    return ParserResult(True, root_node)


@dataclass
class InterpreterResult:
    was_successful: bool
    output: int = 0
    error_message: str = ""


def report_error_for_interpreter(reason_for_error: str) -> InterpreterResult:
    unsuccessful_interpreter_result = InterpreterResult(False, error_message=reason_for_error)
    return unsuccessful_interpreter_result


def interpret_node(node: Union[ExpressionNode, TermNode, FactorNode]) -> InterpreterResult:

    DIVISION_BY_ZERO = "You cannot divide by zero"

    if isinstance(node, FactorNode):
            
        number_as_int = int(node.number)
        factor_node_result = InterpreterResult(True, number_as_int)

        return factor_node_result


    elif isinstance(node, TermNode):

        first_factor: InterpreterResult = interpret_node(node.first_factor_node)

        if (node.operator is None) or (node.second_factor_node is None):
            simple_term_node_result = InterpreterResult(True, first_factor.output)
            return simple_term_node_result

        second_factor: InterpreterResult = interpret_node(node.second_factor_node)

        if node.operator == ArithmeticOperator.DIVIDE:
            
            if second_factor.output == 0:
                unsuccessful_result: InterpreterResult = report_error_for_interpreter(DIVISION_BY_ZERO)
                return unsuccessful_result
            
            output = first_factor.output / second_factor.output
        else:
            output = first_factor.output * second_factor.output
    
        output = int(output)

        complex_term_node_result = InterpreterResult(True, output)
        return complex_term_node_result


    elif isinstance(node, ExpressionNode):

        if node.additional_expression_node is None:
            single_term: InterpreterResult = interpret_node(node.single_term_node)

            if not single_term.was_successful:
                return single_term

            expression_node_result = InterpreterResult(True, single_term.output)
            return expression_node_result

        additional_expression: InterpreterResult = interpret_node(
                node.additional_expression_node)

        single_term: InterpreterResult = interpret_node(node.single_term_node)

        if node.operator == ArithmeticOperator.PLUS:
            output = additional_expression.output + single_term.output
        else:
            output = additional_expression.output - single_term.output

        output = int(output)

        complex_expression_node_result = InterpreterResult(True, output)
        return complex_expression_node_result


    error_message = "This code should be unreachable"
    this_result_should_be_unreachable = InterpreterResult(False, error_message=error_message)

    return this_result_should_be_unreachable


def main():
    PROMPT = "? - "

    while True:
        user_input = input(PROMPT)

        lexer_result: LexerResult = scan_and_tokenize_input(user_input)

        if not lexer_result.was_successful:
            print(lexer_result.error_message)
            continue

        parser_result: ParserResult = parse_list_of_tokens(lexer_result.tokens)

        if (not parser_result.was_successful) or (parser_result.syntax_tree is None):
            print(parser_result.error_message)
            continue

        interpreter_result: InterpreterResult = interpret_node(parser_result.syntax_tree)

        if not interpreter_result.was_successful:
            print(interpreter_result.error_message)
            continue

        print(interpreter_result.output)


if __name__ == "__main__":
    main()

