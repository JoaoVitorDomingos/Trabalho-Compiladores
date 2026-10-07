# Compilador MiniC — Parte 1

Implementação em Python da primeira etapa do trabalho prático de Construção de um Compilador.

## Escopo

- análise léxica;
- análise sintática por descida recursiva;
- construção da Árvore Sintática Abstrata (AST);
- diagnóstico de erros léxicos e sintáticos com linha e coluna;
- execução pela linha de comando;
- arquivos de teste válidos e inválidos.

A implementação segue a gramática MiniC fornecida no enunciado, sem incluir comentários, strings, vetores, funções, procedimentos ou laços.

## Estrutura

```text
minic_compilador/
├── src/
│   ├── __init__.py
│   ├── ast_nodes.py
│   ├── lexer.py
│   ├── parser.py
│   └── main.py
├── minic_tests/
│   ├── valido_soma.mc
│   ├── valido_condicional.mc
│   ├── valido_logico.mc
│   ├── valido_bloco.mc
│   ├── erro_lexico.mc
│   ├── erro_sintatico.mc
│   └── erro_sintatico_bloco.mc
├── docs/
│   └── relatorio.md
└── README.md
```

## Requisitos

- Python 3.10 ou superior recomendado.
- Nenhuma biblioteca externa é necessária.

## Execução

Na pasta raiz do projeto:

```bash
python src/main.py minic_tests/valido_soma.mc
```

O programa mostra os tokens reconhecidos e, quando a análise é válida, a AST em JSON.

Para testar um erro léxico:

```bash
python src/main.py minic_tests/erro_lexico.mc
```

Para testar um erro sintático:

```bash
python src/main.py minic_tests/erro_sintatico.mc
```

## Observação sobre a gramática

A precedência implementada segue diretamente os níveis da gramática: `||`, `&&`, operadores relacionais, `+/-`, `*//` e fatores/unários. Parênteses alteram a associação da expressão. O operador relacional é opcional e ocorre no máximo uma vez em cada expressão relacional, conforme a produção fornecida.
