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
        type_token = self.advance()
        type_name = type_token.lexeme
        identifiers = [self.expect("IDENTIFIER", "identificador")]
        while self.match("COMMA"):
            identifiers.append(self.expect("IDENTIFIER", "identificador após ','"))
        self.expect("SEMICOLON", "';'")
        node = Declaration(type_name, [token.lexeme for token in identifiers])
        node.line = type_token.line
        node.identifier_lines = {token.lexeme: token.line for token in identifiers}
        return node

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
        identifier_token = self.expect("IDENTIFIER")
        identifier = identifier_token.lexeme
        self.expect("ASSIGN", "'='")
        expression = self.parse_expression()
        self.expect("SEMICOLON", "';'")
        node = Assignment(identifier, expression)
        node.line = identifier_token.line
        node.identifier_line = identifier_token.line
        return node

    def parse_read(self):
        read_token = self.expect("READ")
        self.expect("LPAREN", "'('")
        identifier_tokens = [self.expect("IDENTIFIER", "identificador")]
        while self.match("COMMA"):
            identifier_tokens.append(self.expect("IDENTIFIER", "identificador após ','"))
        self.expect("RPAREN", "')'")
        self.expect("SEMICOLON", "';'")
        node = Read([token.lexeme for token in identifier_tokens])
        node.line = read_token.line
        node.identifier_lines = [token.line for token in identifier_tokens]
        return node

    def parse_write(self):
        write_token = self.expect("WRITE")
        self.expect("LPAREN", "'('")
        expressions = [self.parse_expression()]
        while self.match("COMMA"):
            expressions.append(self.parse_expression())
        self.expect("RPAREN", "')'")
        self.expect("SEMICOLON", "';'")
        node = Write(expressions)
        node.line = write_token.line
        return node

    def parse_if(self):
        if_token = self.expect("IF")
        self.expect("LPAREN", "'('")
        condition = self.parse_expression()
        self.expect("RPAREN", "')'")
        then_block = self.parse_block()
        else_block = None
        if self.match("ELSE"):
            else_block = self.parse_block()
        node = If(condition, then_block, else_block)
        node.line = if_token.line
        return node

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
        while self.check("OR"):
            token = self.advance()
            node = BinaryOp("||", node, self.parse_logical_and())
            node.line = token.line
        return node

    def parse_logical_and(self):
        node = self.parse_relational()
        while self.check("AND"):
            token = self.advance()
            node = BinaryOp("&&", node, self.parse_relational())
            node.line = token.line
        return node

    def parse_relational(self):
        node = self.parse_arithmetic()
        if self.check_any("LT", "LE", "GT", "GE", "EQ", "NE"):
            token = self.advance()
            node = BinaryOp(token.lexeme, node, self.parse_arithmetic())
            node.line = token.line
        return node

    def parse_arithmetic(self):
        node = self.parse_term()
        while self.check_any("PLUS", "MINUS"):
            token = self.advance()
            node = BinaryOp(token.lexeme, node, self.parse_term())
            node.line = token.line
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.check_any("STAR", "SLASH"):
            token = self.advance()
            node = BinaryOp(token.lexeme, node, self.parse_factor())
            node.line = token.line
        return node

    def parse_factor(self):
        if self.check("NOT"):
            token = self.advance()
            node = UnaryOp("!", self.parse_factor())
            node.line = token.line
            return node
        if self.check("MINUS"):
            token = self.advance()
            node = UnaryOp("-", self.parse_factor())
            node.line = token.line
            return node
        if self.check("IDENTIFIER"):
            token = self.advance()
            node = Identifier(token.lexeme)
            node.line = token.line
            return node
        if self.check("NUMBER"):
            token = self.advance()
            node = Number(int(token.lexeme))
            node.line = token.line
            return node
        if self.check("TRUE"):
            token = self.advance()
            node = Boolean(True)
            node.line = token.line
            return node
        if self.check("FALSE"):
            token = self.advance()
            node = Boolean(False)
            node.line = token.line
            return node
        if self.match("LPAREN"):
            expression = self.parse_expression()
            self.expect("RPAREN", "')'")
            return expression
        raise SyntaxError("expressão esperada", self.token)
