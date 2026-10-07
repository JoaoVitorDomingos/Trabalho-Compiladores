from lexer import Token
from ast_nodes import (
    Program, Declaration, Assignment, Read, Write, If, Block,
    BinaryOp, UnaryOp, Identifier, Number, Boolean,
)


class SyntaxError(Exception):
    def __init__(self, message, token):
        super().__init__(f"Erro sintático na linha {token.line}, coluna {token.column}: {message}. Encontrado: {token.lexeme or 'fim do arquivo'}")
        self.line = token.line
        self.column = token.column


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    @property
    def token(self):
        return self.tokens[self.current]

    def advance(self):
        token = self.token
        if self.current < len(self.tokens) - 1:
            self.current += 1
        return token

    def check(self, kind):
        return self.token.kind == kind

    def match(self, *kinds):
        if self.check_any(*kinds):
            return self.advance()
        return None

    def check_any(self, *kinds):
        return self.token.kind in kinds

    def expect(self, kind, description=None):
        if not self.check(kind):
            description = description or kind
            raise SyntaxError(f"esperado {description}", self.token)
        return self.advance()

    def parse(self):
        program = self.parse_program()
        self.expect("EOF", "fim do arquivo")
        return program

    def parse_program(self):
        self.expect("PROGRAM", "'program'")
        name = self.expect("IDENTIFIER", "nome do programa").lexeme
        self.expect("LBRACE", "'{'")

        declarations = []
        while self.check_any("INT", "BOOL"):
            declarations.append(self.parse_declaration())

        commands = []
        while not self.check("RBRACE"):
            if self.check("EOF"):
                raise SyntaxError("esperado '}' para fechar o programa", self.token)
            commands.append(self.parse_command())

        self.expect("RBRACE", "'}'")
        return Program(name, declarations, commands)

    def parse_declaration(self):
        type_name = self.advance().lexeme
        identifiers = [self.expect("IDENTIFIER", "identificador").lexeme]
        while self.match("COMMA"):
            identifiers.append(self.expect("IDENTIFIER", "identificador após ','").lexeme)
        self.expect("SEMICOLON", "';'")
        return Declaration(type_name, identifiers)

    def parse_command(self):
        if self.check("IDENTIFIER"):
            return self.parse_assignment()
        if self.check("READ"):
            return self.parse_read()
        if self.check("WRITE"):
            return self.parse_write()
        if self.check("IF"):
            return self.parse_if()
        if self.check("LBRACE"):
            return self.parse_block()
        raise SyntaxError("comando esperado", self.token)

    def parse_assignment(self):
        identifier = self.expect("IDENTIFIER").lexeme
        self.expect("ASSIGN", "'='")
        expression = self.parse_expression()
        self.expect("SEMICOLON", "';'")
        return Assignment(identifier, expression)

    def parse_read(self):
        self.expect("READ")
        self.expect("LPAREN", "'('")
        identifiers = [self.expect("IDENTIFIER", "identificador").lexeme]
        while self.match("COMMA"):
            identifiers.append(self.expect("IDENTIFIER", "identificador após ','").lexeme)
        self.expect("RPAREN", "')'")
        self.expect("SEMICOLON", "';'")
        return Read(identifiers)

    def parse_write(self):
        self.expect("WRITE")
        self.expect("LPAREN", "'('")
        expressions = [self.parse_expression()]
        while self.match("COMMA"):
            expressions.append(self.parse_expression())
        self.expect("RPAREN", "')'")
        self.expect("SEMICOLON", "';'")
        return Write(expressions)

    def parse_if(self):
        self.expect("IF")
        self.expect("LPAREN", "'('")
        condition = self.parse_expression()
        self.expect("RPAREN", "')'")
        then_block = self.parse_block()
        else_block = None
        if self.match("ELSE"):
            else_block = self.parse_block()
        return If(condition, then_block, else_block)

    def parse_block(self):
        self.expect("LBRACE", "'{'")
        commands = []
        while not self.check("RBRACE"):
            if self.check("EOF"):
                raise SyntaxError("esperado '}' para fechar o bloco", self.token)
            commands.append(self.parse_command())
        self.expect("RBRACE", "'}'")
        return Block(commands)

    def parse_expression(self):
        return self.parse_logical_or()

    def parse_logical_or(self):
        node = self.parse_logical_and()
        while self.match("OR"):
            node = BinaryOp("||", node, self.parse_logical_and())
        return node

    def parse_logical_and(self):
        node = self.parse_relational()
        while self.match("AND"):
            node = BinaryOp("&&", node, self.parse_relational())
        return node

    def parse_relational(self):
        node = self.parse_arithmetic()
        if self.check_any("LT", "LE", "GT", "GE", "EQ", "NE"):
            operator = self.advance().lexeme
            node = BinaryOp(operator, node, self.parse_arithmetic())
        return node

    def parse_arithmetic(self):
        node = self.parse_term()
        while self.check_any("PLUS", "MINUS"):
            operator = self.advance().lexeme
            node = BinaryOp(operator, node, self.parse_term())
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.check_any("STAR", "SLASH"):
            operator = self.advance().lexeme
            node = BinaryOp(operator, node, self.parse_factor())
        return node

    def parse_factor(self):
        if self.match("NOT"):
            return UnaryOp("!", self.parse_factor())
        if self.match("MINUS"):
            return UnaryOp("-", self.parse_factor())
        if self.check("IDENTIFIER"):
            return Identifier(self.advance().lexeme)
        if self.check("NUMBER"):
            return Number(int(self.advance().lexeme))
        if self.match("TRUE"):
            return Boolean(True)
        if self.match("FALSE"):
            return Boolean(False)
        if self.match("LPAREN"):
            expression = self.parse_expression()
            self.expect("RPAREN", "')'")
            return expression
        raise SyntaxError("expressão esperada", self.token)
