from typing import Union
from .ast import (
    ExpressionNode,
    TermNode,
    FactorNode,
    InterpreterResult,
    ArithmeticOperator,
)

def report_error_for_interpreter(reason_for_error: str) -> InterpreterResult:
    return InterpreterResult(False, error_message=reason_for_error)

def interpret_node(node: Union[ExpressionNode, TermNode, FactorNode]) -> InterpreterResult:
    if isinstance(node, FactorNode):
        if node.nested_expression is not None:
            nested_result = interpret_node(node.nested_expression)
            if not nested_result.was_successful:
                return nested_result
            value = nested_result.output * node.sign
        else:
            value = int(node.number) * node.sign
        return InterpreterResult(True, int(value))

    if isinstance(node, TermNode):
        first_factor = interpret_node(node.first_factor_node)
        if not first_factor.was_successful:
            return first_factor
        if (node.operator is None) or (node.second_factor_node is None):
            return InterpreterResult(True, first_factor.output)

        second_factor = interpret_node(node.second_factor_node)
        if not second_factor.was_successful:
            return second_factor

        if node.operator == ArithmeticOperator.DIVIDE:
            if second_factor.output == 0:
                return report_error_for_interpreter("You cannot divide by zero")
            output = first_factor.output / second_factor.output
        else:
            output = first_factor.output * second_factor.output

        return InterpreterResult(True, int(output))

    if isinstance(node, ExpressionNode):
        left = interpret_node(node.single_term_node)
        if not left.was_successful:
            return left
        if node.additional_expression_node is None:
            return InterpreterResult(True, left.output)

        right = interpret_node(node.additional_expression_node)
        if not right.was_successful:
            return right

        if node.operator == ArithmeticOperator.PLUS:
            return InterpreterResult(True, int(left.output + right.output))
        else:
            return InterpreterResult(True, int(left.output - right.output))

    return InterpreterResult(False, error_message="Interpreter reached unreachable code")

