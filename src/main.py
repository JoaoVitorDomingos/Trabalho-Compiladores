import json
import sys
from pathlib import Path

from lexer import Lexer, LexicalError
from parser import Parser, SyntaxError
from ast_nodes import ast_to_dict


def print_tokens(tokens):
    print("=== TOKENS ===")
    for token in tokens:
        if token.kind != "EOF":
            print(f"{token.line}:{token.column}  {token.kind:<12} {token.lexeme!r}")
    print()


def main():
    if len(sys.argv) != 2:
        print("Uso: python src/main.py <arquivo.mc>")
        return 2

    source_path = Path(sys.argv[1])
    if not source_path.is_file():
        print(f"Arquivo não encontrado: {source_path}")
        return 2

    try:
        source = source_path.read_text(encoding="utf-8")
        tokens = Lexer().tokenize(source)
        print_tokens(tokens)
        tree = Parser(tokens).parse()
    except (LexicalError, SyntaxError, UnicodeDecodeError) as exc:
        print(str(exc))
        return 1

    print("=== AST ===")
    print(json.dumps(ast_to_dict(tree), ensure_ascii=False, indent=2))
    print("\nAnálise concluída com sucesso.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
