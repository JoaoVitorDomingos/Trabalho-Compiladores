from dataclasses import dataclass


class LexicalError(Exception):
    def __init__(self, message, line, column):
        super().__init__(f"Erro léxico na linha {line}, coluna {column}: {message}")
        self.line = line
        self.column = column


@dataclass(frozen=True)
class Token:
    kind: str
    lexeme: str
    line: int
    column: int

    def __repr__(self):
        return f"Token({self.kind!r}, {self.lexeme!r}, {self.line}:{self.column})"


class Lexer:
    KEYWORDS = {
        "program": "PROGRAM",
        "int": "INT",
        "bool": "BOOL",
        "if": "IF",
        "else": "ELSE",
        "read": "READ",
        "write": "WRITE",
        "true": "TRUE",
        "false": "FALSE",
    }

    TWO_CHAR_OPERATORS = {
        "<=": "LE",
        ">=": "GE",
        "==": "EQ",
        "!=": "NE",
        "&&": "AND",
        "||": "OR",
    }

    ONE_CHAR = {
        "+": "PLUS",
        "-": "MINUS",
        "*": "STAR",
        "/": "SLASH",
        "<": "LT",
        ">": "GT",
        "!": "NOT",
        "=": "ASSIGN",
        "(": "LPAREN",
        ")": "RPAREN",
        "{": "LBRACE",
        "}": "RBRACE",
        ";": "SEMICOLON",
        ",": "COMMA",
    }

    def tokenize(self, source):
        tokens = []
        i = 0
        line = 1
        column = 1

        while i < len(source):
            ch = source[i]

            if ch in " \t\r":
                i += 1
                column += 1
                continue
            if ch == "\n":
                i += 1
                line += 1
                column = 1
                continue

            start_line, start_column = line, column

            if ch.isalpha():
                start = i
                while i < len(source) and (source[i].isalnum() or source[i] == "_"):
                    i += 1
                    column += 1
                lexeme = source[start:i]
                kind = self.KEYWORDS.get(lexeme, "IDENTIFIER")
                tokens.append(Token(kind, lexeme, start_line, start_column))
                continue

            if ch.isdigit():
                start = i
                while i < len(source) and source[i].isdigit():
                    i += 1
                    column += 1
                tokens.append(Token("NUMBER", source[start:i], start_line, start_column))
                continue

            pair = source[i:i + 2]
            if pair in self.TWO_CHAR_OPERATORS:
                tokens.append(Token(self.TWO_CHAR_OPERATORS[pair], pair, start_line, start_column))
                i += 2
                column += 2
                continue

            if ch in self.ONE_CHAR:
                tokens.append(Token(self.ONE_CHAR[ch], ch, start_line, start_column))
                i += 1
                column += 1
                continue

            raise LexicalError(f"símbolo não reconhecido {ch!r}", start_line, start_column)

        tokens.append(Token("EOF", "", line, column))
        return tokens
