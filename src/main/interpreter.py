from typing import Union
from dataclasses import dataclass
from .ast import (
    ExpressionNode,
    TermNode,
    FactorNode,
    ArithmeticOperator,
)


@dataclass
class InterpreterResult:
    """
    Represents the result of interpreting an AST node.

    - error_message will always be an empty string if was_successful is True.
    """

    was_successful: bool
    output: int = 0
    error_message: str = ""


def report_error_for_interpreter(reason_for_error: str) -> InterpreterResult:
    """
    Clarity function to report an error from the interpreter.
    """

    return InterpreterResult(False, error_message=reason_for_error)


def interpret_node(node: Union[ExpressionNode, TermNode, FactorNode]) -> InterpreterResult:
    """
    The primary interpreter function that recursively evaluates AST nodes.
    """

    # handle factor nodes
    if isinstance(node, FactorNode):
        if node.nested_expression is not None:
            nested_result = interpret_node(node.nested_expression)
            if not nested_result.was_successful:
                return nested_result

            value = nested_result.output * node.sign
        else:
            value = int(node.number) * node.sign

        return InterpreterResult(True, int(value))

    # handle term nodes
    if isinstance(node, TermNode):
        first_factor = interpret_node(node.first_factor_node)
        if not first_factor.was_successful:
            return first_factor
        if (node.operator is None) or (node.second_factor_node is None):
            return InterpreterResult(True, first_factor.output)

        second_factor = interpret_node(node.second_factor_node)
        if not second_factor.was_successful:
            return second_factor

        # check division by zero
        if node.operator == ArithmeticOperator.DIVIDE:
            if second_factor.output == 0:
                return report_error_for_interpreter("You cannot divide by zero")
            output = first_factor.output / second_factor.output
        else:
            output = first_factor.output * second_factor.output

        return InterpreterResult(True, int(output))

    # handle expression nodes
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

    # Should be unreachable but never hurts to be safe
    return InterpreterResult(False, error_message="Interpreter reached unreachable code")
