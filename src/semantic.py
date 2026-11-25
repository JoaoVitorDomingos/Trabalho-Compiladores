"""Análise semântica e tabela de símbolos da MiniC."""

from dataclasses import dataclass

from ast_nodes import (
    Assignment, BinaryOp, Block, Boolean, Declaration, Identifier, If, Number,
    Program, Read, UnaryOp, Write,
)


INT = "int"
BOOL = "bool"


@dataclass
class Symbol:
    name: str
    type_name: str
    line: int


class SymbolTable:
    """Tabela plana: a MiniC não define escopo local para blocos."""

    def __init__(self):
        self.symbols = {}

    def declare(self, name, type_name, line):
        if name in self.symbols:
            return False
        self.symbols[name] = Symbol(name, type_name, line)
        return True

    def lookup(self, name):
        return self.symbols.get(name)


class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors = []

    def error(self, node, message, line=None):
        line = line or getattr(node, "line", None)
        where = f" na linha {line}" if line else ""
        self.errors.append(f"Erro semântico{where}: {message}")

    def analyze(self, program):
        self.errors = []
        self.symbol_table = SymbolTable()

        for declaration in program.declarations:
            for name in declaration.identifiers:
                line = declaration.identifier_lines.get(name, declaration.line)
                if not self.symbol_table.declare(name, declaration.type_name, line):
                    self.error(declaration, f"variável '{name}' declarada mais de uma vez", line)

        for command in program.commands:
            self.check_command(command)
        return self.errors

    def variable_type(self, name, node, line=None):
        symbol = self.symbol_table.lookup(name)
        if symbol is None:
            self.error(node, f"variável '{name}' utilizada sem declaração", line)
            return None
        return symbol.type_name

    def check_command(self, command):
        if isinstance(command, Assignment):
            target_type = self.variable_type(command.identifier, command, command.identifier_line)
            expression_type = self.expression_type(command.expression)
            if target_type and expression_type and target_type != expression_type:
                self.error(command, f"atribuição incompatível: '{command.identifier}' é {target_type}, mas a expressão é {expression_type}")
        elif isinstance(command, Read):
            for name, line in zip(command.identifiers, command.identifier_lines):
                self.variable_type(name, command, line)
        elif isinstance(command, Write):
            for expression in command.expressions:
                self.expression_type(expression)
        elif isinstance(command, If):
            condition_type = self.expression_type(command.condition)
            if condition_type and condition_type != BOOL:
                self.error(command, f"a condição do if deve ser bool, mas é {condition_type}")
            self.check_command(command.then_block)
            if command.else_block:
                self.check_command(command.else_block)
        elif isinstance(command, Block):
            for nested in command.commands:
                self.check_command(nested)

    def expression_type(self, expression):
        if isinstance(expression, Number):
            return INT
        if isinstance(expression, Boolean):
            return BOOL
        if isinstance(expression, Identifier):
            return self.variable_type(expression.name, expression)
        if isinstance(expression, UnaryOp):
            operand_type = self.expression_type(expression.operand)
            expected = BOOL if expression.operator == "!" else INT
            if operand_type and operand_type != expected:
                self.error(expression, f"operador '{expression.operator}' exige operando {expected}, mas recebeu {operand_type}")
                return None
            return expected if operand_type else None
        if isinstance(expression, BinaryOp):
            left_type = self.expression_type(expression.left)
            right_type = self.expression_type(expression.right)
            if left_type is None or right_type is None:
                return None
            operator = expression.operator
            if operator in {"+", "-", "*", "/"}:
                if left_type != INT or right_type != INT:
                    self.error(expression, f"operador '{operator}' exige operandos int, mas recebeu {left_type} e {right_type}")
                    return None
                return INT
            if operator in {"<", "<=", ">", ">="}:
                if left_type != INT or right_type != INT:
                    self.error(expression, f"operador '{operator}' exige operandos int, mas recebeu {left_type} e {right_type}")
                    return None
                return BOOL
            if operator in {"==", "!="}:
                if left_type != right_type:
                    self.error(expression, f"operador '{operator}' exige operandos do mesmo tipo, mas recebeu {left_type} e {right_type}")
                    return None
                return BOOL
            if operator in {"&&", "||"}:
                if left_type != BOOL or right_type != BOOL:
                    self.error(expression, f"operador '{operator}' exige operandos bool, mas recebeu {left_type} e {right_type}")
                    return None
                return BOOL
        return None
