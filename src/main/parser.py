from typing import List, Optional, AnyStr
from .ast import (
    Token,
    ParserResult,
    NodeResult,
    ExpressionNode,
    TermNode,
    FactorNode,
    ArithmeticOperator,
    NUMBER_TOKEN_TYPE,
    PLUS_TOKEN_TYPE,
    MINUS_TOKEN_TYPE,
    MULTIPLY_TOKEN_TYPE,
    DIVIDE_TOKEN_TYPE,
    LPAREN_TOKEN_TYPE,
    RPAREN_TOKEN_TYPE,
)

def parse_list_of_tokens(tokens: List[Token]) -> ParserResult:
    class ParserErrorReason:
        UNEXPECTED_TOKEN_TYPE = "Unexpected Token Type, {0}"
        VALUE_IS_NULL = "Found A Null Value; {0} is Null"
        UNEXPECTED_TYPE = "Unexpected Node of Type, {0}"

    def report_error(unexpected_token_type: Optional[str] = None,
                     unexpected_null: Optional[AnyStr] = None,
                     unexpected_type: Optional[AnyStr] = None) -> NodeResult:
        error_message = ""
        if unexpected_token_type is not None:
            error_message = ParserErrorReason.UNEXPECTED_TOKEN_TYPE.format(unexpected_token_type)
        if unexpected_null is not None:
            error_message = ParserErrorReason.VALUE_IS_NULL.format(unexpected_null)
        if unexpected_type is not None:
            error_message = ParserErrorReason.UNEXPECTED_TYPE.format(unexpected_type)
        return NodeResult(False, error_message=error_message)

    # forward declarations via nested functions
    def parse_tokens_for_expression(tokens: List[Token]) -> NodeResult:
        term_result = parse_tokens_for_term(tokens)
        if not term_result.was_successful:
            return term_result
        if not isinstance(term_result.node, TermNode):
            return report_error(unexpected_type=str(type(term_result.node)))

        expr_node = ExpressionNode(term_result.node)
        remaining = term_result.tokens or []

        while remaining and remaining[0].token_type in (PLUS_TOKEN_TYPE, MINUS_TOKEN_TYPE):
            op_token = remaining[0]
            remaining = remaining[1:]
            op = ArithmeticOperator.PLUS if op_token.token_type == PLUS_TOKEN_TYPE else ArithmeticOperator.MINUS

            next_term_result = parse_tokens_for_term(remaining)
            if not next_term_result.was_successful:
                return next_term_result
            if not isinstance(next_term_result.node, TermNode):
                return report_error(unexpected_type=str(type(next_term_result.node)))

            # build left-associative expression
            expr_node = ExpressionNode(expr_node, op, ExpressionNode(next_term_result.node))
            remaining = next_term_result.tokens or []

        return NodeResult(True, remaining, expr_node)

    def parse_tokens_for_term(tokens: List[Token]) -> NodeResult:
        factor_result = parse_tokens_for_factor(tokens)
        if not factor_result.was_successful:
            return factor_result
        if not isinstance(factor_result.node, FactorNode):
            return report_error(unexpected_type=str(type(factor_result.node)))

        term_node = TermNode(factor_result.node)
        remaining = factor_result.tokens or []

        while remaining and remaining[0].token_type in (MULTIPLY_TOKEN_TYPE, DIVIDE_TOKEN_TYPE):
            op_token = remaining[0]
            remaining = remaining[1:]
            op = ArithmeticOperator.MULTIPLY if op_token.token_type == MULTIPLY_TOKEN_TYPE else ArithmeticOperator.DIVIDE

            second_factor_result = parse_tokens_for_factor(remaining)
            if not second_factor_result.was_successful:
                return second_factor_result
            if not isinstance(second_factor_result.node, FactorNode):
                return report_error(unexpected_type=str(type(second_factor_result.node)))

            term_node = TermNode(term_node, op, second_factor_result.node)
            remaining = second_factor_result.tokens or []

        return NodeResult(True, remaining, term_node)

    def parse_tokens_for_primary(tokens: List[Token]) -> NodeResult:
        if not tokens:
            return report_error(unexpected_null="No tokens for primary")
        current = tokens[0]
        if current.token_type == NUMBER_TOKEN_TYPE:
            return NodeResult(True, tokens[1:], FactorNode(sign=1, number=current.token_value))
        if current.token_type == LPAREN_TOKEN_TYPE:
            inner = tokens[1:]
            expr_result = parse_tokens_for_expression(inner)
            if not expr_result.was_successful:
                return expr_result
            if not expr_result.tokens:
                return report_error(unexpected_null="Missing closing parenthesis")
            if expr_result.tokens[0].token_type != RPAREN_TOKEN_TYPE:
                return report_error(unexpected_token_type=expr_result.tokens[0].token_type)
            return NodeResult(True, expr_result.tokens[1:], FactorNode(sign=1, nested_expression=expr_result.node))
        return report_error(unexpected_token_type=current.token_type)

    def parse_tokens_for_factor(tokens: List[Token]) -> NodeResult:
        if not tokens:
            return report_error(unexpected_null="No tokens for factor")
        current = tokens[0]
        if current.token_type in (PLUS_TOKEN_TYPE, MINUS_TOKEN_TYPE):
            op_token = current
            remaining = tokens[1:]
            inner_result = parse_tokens_for_factor(remaining)
            if not inner_result.was_successful:
                return inner_result
            if not isinstance(inner_result.node, FactorNode):
                return report_error(unexpected_type=str(type(inner_result.node)))
            inner_node: FactorNode = inner_result.node
            sign = -inner_node.sign if op_token.token_type == MINUS_TOKEN_TYPE else inner_node.sign
            return NodeResult(True, inner_result.tokens, FactorNode(sign=sign, number=inner_node.number, nested_expression=inner_node.nested_expression))
        # primary
        return parse_tokens_for_primary(tokens)

    # start parse
    root_node_result = parse_tokens_for_expression(tokens)
    if not root_node_result.was_successful:
        return ParserResult(False, error_message=root_node_result.error_message)
    if not isinstance(root_node_result.node, ExpressionNode):
        err = report_error(unexpected_type=str(type(root_node_result.node)))
        return ParserResult(False, error_message=err.error_message)
    return ParserResult(True, root_node_result.node)

