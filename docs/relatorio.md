# Relatório Técnico — Compilador MiniC (Parte 1)

## 1. Objetivo

O objetivo desta etapa é implementar, em Python, um compilador para a linguagem MiniC, contemplando análise léxica, análise sintática e construção de uma Árvore Sintática Abstrata (AST). A implementação foi feita sem bibliotecas externas, utilizando um analisador léxico manual e um analisador sintático descendente recursivo.

## 2. Linguagem MiniC

A MiniC possui sintaxe semelhante à linguagem C, mas com um conjunto reduzido de recursos. A linguagem possui os tipos `int` e `bool`, os valores `true` e `false`, comandos de atribuição, leitura, escrita, condicionais e blocos. Não são previstos strings, vetores, funções, procedimentos ou estruturas de repetição.

Os identificadores começam por uma letra e podem continuar com letras, dígitos ou `_`. Números são sequências de dígitos decimais. Espaços, tabulações e quebras de linha são ignorados. O sinal `-` é tratado como operador, inclusive no caso de negação aritmética.

## 3. Análise léxica

O arquivo `src/lexer.py` percorre o programa caractere a caractere e produz uma sequência de tokens. São reconhecidos:

- palavras reservadas: `program`, `int`, `bool`, `if`, `else`, `read`, `write`, `true`, `false`;
- identificadores;
- números inteiros;
- operadores de um e dois caracteres;
- delimitadores `(`, `)`, `{`, `}`, `;` e `,`.

Cada token armazena tipo, lexema, linha e coluna. Quando um símbolo não pertence à linguagem, é lançada uma exceção `LexicalError`, informando a posição do problema.

## 4. Análise sintática

O arquivo `src/parser.py` implementa a gramática por descida recursiva. Cada produção relevante da gramática é representada por um método do parser.

A estrutura principal é analisada na seguinte ordem: palavra `program`, identificador do programa, abertura do bloco, declarações, comandos e fechamento do programa. As declarações são processadas antes dos comandos, conforme a especificação.

As expressões são divididas em níveis para preservar a precedência: expressão lógica com `||`, expressão `&&`, expressão relacional, expressão aritmética, termo e fator. Os fatores também contemplam identificadores, números, booleanos, expressões entre parênteses e operadores unários `!` e `-`.

Quando a sequência de tokens não corresponde à gramática, é lançada `SyntaxError`, contendo linha, coluna e uma descrição do token esperado.

## 5. Árvore Sintática Abstrata

O arquivo `src/ast_nodes.py` define classes para representar a estrutura essencial do programa. Foram utilizadas estruturas `dataclass` para manter a representação simples e modular.

Entre os nós estão `Program`, `Declaration`, `Assignment`, `Read`, `Write`, `If`, `Block`, `BinaryOp`, `UnaryOp`, `Identifier`, `Number` e `Boolean`.

A AST não mantém elementos que servem apenas para a análise sintática, como ponto e vírgula, vírgulas e parênteses. Assim, ela fica adequada para utilização nas próximas etapas do compilador.

## 6. Interface de execução

O arquivo `src/main.py` recebe o arquivo MiniC pela linha de comando. O uso é:

```text
python src/main.py programa.mc
```

Após a análise léxica, os tokens são exibidos. Se a análise sintática for concluída, a AST é impressa em formato JSON. Em caso de erro, a mensagem informa a posição do problema.

## 7. Testes

Foram incluídos programas válidos que exercitam:

- declarações múltiplas;
- leitura de uma ou várias variáveis;
- atribuições;
- precedência de operadores;
- valores booleanos;
- operadores lógicos, relacionais e aritméticos;
- expressões entre parênteses;
- operadores unários;
- `if` com e sem `else`;
- blocos.

Também foram incluídos testes inválidos para erro léxico e erros sintáticos, incluindo ausência de `;` e fechamento incorreto de bloco.

## 8. Conclusão

A primeira etapa do compilador MiniC foi implementada de forma modular. O lexer é responsável exclusivamente pela transformação do texto em tokens, o parser pela validação sintática e construção da AST, e o módulo principal pela interface de execução. A separação facilita a evolução do projeto para as próximas etapas, nas quais poderão ser adicionadas análise semântica, tabela de símbolos e geração de código intermediário.
