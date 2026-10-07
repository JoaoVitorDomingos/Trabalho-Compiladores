from dataclasses import dataclass, field


@dataclass
class Program:
    name: str
    declarations: list = field(default_factory=list)
    commands: list = field(default_factory=list)


@dataclass
class Declaration:
    type_name: str
    identifiers: list


@dataclass
class Assignment:
    identifier: str
    expression: object


@dataclass
class Read:
    identifiers: list


@dataclass
class Write:
    expressions: list


@dataclass
class If:
    condition: object
    then_block: object
    else_block: object = None


@dataclass
class Block:
    commands: list


@dataclass
class BinaryOp:
    operator: str
    left: object
    right: object


@dataclass
class UnaryOp:
    operator: str
    operand: object


@dataclass
class Identifier:
    name: str


@dataclass
class Number:
    value: int


@dataclass
class Boolean:
    value: bool


def ast_to_dict(node):
    if node is None:
        return None
    if isinstance(node, list):
        return [ast_to_dict(item) for item in node]
    if hasattr(node, "__dataclass_fields__"):
        result = {"node": type(node).__name__}
        for name in node.__dataclass_fields__:
            result[name] = ast_to_dict(getattr(node, name))
        return result
    return node
