import unittest
from main.lexer import scan_and_tokenize_input
from main.parser import parse_list_of_tokens
from main.interpreter import interpret_node

"""
Tests that show the full implementation of the calculator grammar is working as expected.
Each test runs the full pipeline: lexing, parsing, interpreting.
"""

class CalculatorGrammarTests(unittest.TestCase):

    def run_full_pipeline(self, expr: str):
        """
        Helper: run lexer -> parser -> interpreter and return all results.
        """

        lexer_result = scan_and_tokenize_input(expr)
        self.assertTrue(lexer_result.was_successful, f"Lexer failed for: {expr} ({getattr(lexer_result, 'error_message', '')})")

        parser_result = parse_list_of_tokens(lexer_result.tokens)
        self.assertTrue(parser_result.was_successful, f"Parser failed for: {expr} ({parser_result.error_message})")
        self.assertIsNotNone(parser_result.syntax_tree, f"No AST produced for: {expr}")

        interpreter_result = interpret_node(parser_result.syntax_tree)

        return lexer_result, parser_result, interpreter_result

    def test_001_zero(self):
        _, _, result = self.run_full_pipeline("0")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, 0)

    def test_002_single_digit(self):
        _, _, result = self.run_full_pipeline("5")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, 5)

    def test_003_whitespace_number(self):
        _, _, result = self.run_full_pipeline("   42  ")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, 42)

    def test_004_unary_negative(self):
        _, _, result = self.run_full_pipeline("-5")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, -5)

    def test_005_unary_positive(self):
        _, _, result = self.run_full_pipeline("+7")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, 7)

    def test_006_double_unary(self):
        _, _, result = self.run_full_pipeline("--5")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, 5)

    def test_007_mixed_unary(self):
        _, _, result = self.run_full_pipeline("-+5")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, -5)

    def test_008_addition(self):
        _, _, result = self.run_full_pipeline("5+3")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, 8)

    def test_009_subtraction(self):
        _, _, result = self.run_full_pipeline("10-2")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, 8)

    def test_010_sub_negative_result(self):
        _, _, result = self.run_full_pipeline("5-10")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, -5)

    def test_011_sub_positive_result(self):
        _, _, result = self.run_full_pipeline("10-5")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, 5)

    def test_012_multiplication(self):
        _, _, result = self.run_full_pipeline("5*2")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, 10)

    def test_013_division(self):
        _, _, result = self.run_full_pipeline("20/4")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, 5)

    def test_014_chained_multiplication(self):
        _, _, result = self.run_full_pipeline("5*2*3*1")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, 30)

    def test_015_chained_division(self):
        _, _, result = self.run_full_pipeline("100/5/2")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, 10)

    def test_016_precedence_mul_over_add(self):
        _, _, result = self.run_full_pipeline("2+3*4")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, 14)

    def test_017_parentheses_change_precedence(self):
        _, _, result = self.run_full_pipeline("(2+3)*4")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, 20)

    def test_018_unary_with_parentheses_and_mul(self):
        _, _, result = self.run_full_pipeline("-(2+3)*4")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, -20)

    def test_019_unary_and_negative_factor(self):
        _, _, result = self.run_full_pipeline("-(2+3)*-4")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, 20)

    def test_020_add_with_unary(self):
        _, _, result = self.run_full_pipeline("3 + -2")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, 1)

    def test_021_sub_with_unary(self):
        _, _, result = self.run_full_pipeline("3 - -2")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, 5)

    def test_022_mul_with_unary(self):
        _, _, result = self.run_full_pipeline("3 * -2")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, -6)

    def test_023_double_negative_mul(self):
        _, _, result = self.run_full_pipeline("-3 * -2")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, 6)

    def test_024_mixed_mul_div(self):
        _, _, result = self.run_full_pipeline("4/2*3")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, 6)

    def test_025_division_non_integer_result_truncates(self):
        _, _, result = self.run_full_pipeline("4/(2*3)")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, 0)

    def test_026_complex_nested_example(self):
        expr = "7 + 3 * (10 / (12 / (3 + 1) - 1))"
        _, _, result = self.run_full_pipeline(expr)
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, 22)

    def test_027_deep_parenthesis(self):
        _, _, result = self.run_full_pipeline("((2))")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, 2)

    def test_028_unary_on_parentheses(self):
        _, _, result = self.run_full_pipeline("+(5)")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, 5)

    def test_029_unary_inside_parentheses(self):
        _, _, result = self.run_full_pipeline("-(+5)")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, -5)

    def test_030_mixed_ops_order(self):
        _, _, result = self.run_full_pipeline("0-3*4+2")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, -10)

    def test_031_long_add_chain(self):
        _, _, result = self.run_full_pipeline("1+2+3+4+5")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, 15)

    def test_032_left_associative_sub(self):
        _, _, result = self.run_full_pipeline("10-1-2-3")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, 4)

    def test_033_multiple_mul_add(self):
        _, _, result = self.run_full_pipeline("2*3+4*5")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, 26)

    def test_034_nested_parentheses_multiplication(self):
        _, _, result = self.run_full_pipeline("2*(3+4)*5")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, 70)

    def test_035_multi_digit_numbers(self):
        _, _, result = self.run_full_pipeline("12 + 34")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, 46)

    def test_036_whitespace_and_tabs(self):
        _, _, result = self.run_full_pipeline("   6\t* 7 ")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, 42)

    def test_037_unary_with_spaces_between(self):
        _, _, result = self.run_full_pipeline("- - 10")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, 10)

    def test_038_nested_subtraction(self):
        _, _, result = self.run_full_pipeline("5 + (6 - (3 + 1))")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, 7)

    def test_039_mixed_nested_and_mult(self):
        _, _, result = self.run_full_pipeline("5+(6-(3+1))*2")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, 9)

    def test_040_double_nested_parentheses(self):
        _, _, result = self.run_full_pipeline("((1+2)*(3+4))")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, 21)

    def test_041_mixed_precedence(self):
        _, _, result = self.run_full_pipeline("1+2*3-4/2")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, 5)

    def test_042_division_truncation(self):
        _, _, result = self.run_full_pipeline("8/3")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, 2)

    def test_043_parenthesis_with_division(self):
        _, _, result = self.run_full_pipeline("8/(3)")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, 2)

    def test_044_negative_division(self):
        _, _, result = self.run_full_pipeline("-8/3")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, -2)

    def test_045_divide_by_negative(self):
        _, _, result = self.run_full_pipeline("9/ -2")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, -4)

    def test_046_long_alternating_chain(self):
        expr = "1-2+3-4+5-6+7-8+9"
        _, _, result = self.run_full_pipeline(expr)
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, 5)

    def test_047_power_of_two_chain(self):
        _, _, result = self.run_full_pipeline("2*2*2*2*2")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, 32)

    def test_048_combined_complex_expression(self):
        _, _, result = self.run_full_pipeline("2+3*4-5*(6-4)")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, 4)

    def test_049_many_wrapped_parentheses(self):
        _, _, result = self.run_full_pipeline("(((((5)))))")
        self.assertTrue(result.was_successful)
        self.assertEqual(result.output, 5)

    def test_050_division_by_zero_error(self):
        lexer_result = scan_and_tokenize_input("1/0")
        self.assertTrue(lexer_result.was_successful)

        parser_result = parse_list_of_tokens(lexer_result.tokens)
        self.assertTrue(parser_result.was_successful)
        self.assertIsNotNone(parser_result.syntax_tree)

        interpreter_result = interpret_node(parser_result.syntax_tree)
        self.assertFalse(interpreter_result.was_successful)
        self.assertEqual(interpreter_result.error_message, "You cannot divide by zero")


if __name__ == '__main__':
    unittest.main()
