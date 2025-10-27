import re
from typing import List, Union
from .ast import Token, LexerResult
from .ast import (
    NUMBER_TOKEN_TYPE,
    PLUS_TOKEN_TYPE,
    MINUS_TOKEN_TYPE,
    MULTIPLY_TOKEN_TYPE,
    DIVIDE_TOKEN_TYPE,
    WHITESPACE_TOKEN_TYPE,
    LPAREN_TOKEN_TYPE,
    RPAREN_TOKEN_TYPE,
    TokenType,
)

# ordered patterns; whitespace is skipped
token_patterns = {
    r"\d+": NUMBER_TOKEN_TYPE,
    r"\+": PLUS_TOKEN_TYPE,
    r"\-": MINUS_TOKEN_TYPE,
    r"\*": MULTIPLY_TOKEN_TYPE,
    r"/": DIVIDE_TOKEN_TYPE,
    r"\(": LPAREN_TOKEN_TYPE,
    r"\)": RPAREN_TOKEN_TYPE,
    r"\s": WHITESPACE_TOKEN_TYPE,
}

def scan_and_tokenize_input(user_input: str) -> LexerResult:
    def report_error(unknown_character: str) -> LexerResult:
        ERROR_MESSAGE = "Found an unknown character, '{0}'"
        return LexerResult(False, error_message=ERROR_MESSAGE.format(unknown_character))

    tokens: List[Token] = []
    position = 0
    length_of_input = len(user_input)

    while position < length_of_input:
        match: Union[re.Match[str], None] = None
        sliced_input = user_input[position:]

        for pattern in token_patterns.keys():
            match = re.match(pattern, sliced_input)
            if match is not None:
                token_type: TokenType = token_patterns[pattern]
                if token_type == WHITESPACE_TOKEN_TYPE:
                    # skip whitespace
                    break
                token_value = match.group(0)
                tokens.append(Token(token_type, token_value))
                break

        if match is None:
            return report_error(user_input[position])
        position += match.end()

    return LexerResult(True, tokens)

