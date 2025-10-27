from main.lexer import scan_and_tokenize_input
from main.parser import parse_list_of_tokens
from main.interpreter import interpret_node
from main.ast import LexerResult, ParserResult, InterpreterResult

def main():
    PROMPT = ">>> "
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
