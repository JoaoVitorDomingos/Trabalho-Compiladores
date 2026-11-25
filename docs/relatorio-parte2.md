# Relatório Técnico — Compilador MiniC (Parte 2)

## 1. Objetivo

Esta etapa estende o compilador MiniC da Parte 1 com análise semântica, integrada à análise léxica e sintática já existentes. O compilador agora valida declarações e tipos antes de apresentar a AST como resultado de sucesso.

## 2. Tabela de símbolos

O módulo `src/semantic.py` implementa `SymbolTable`, que registra cada variável declarada, seu tipo (`int` ou `bool`) e a linha da declaração. A MiniC deste trabalho não define escopos locais para blocos; por isso, a tabela é única para o programa. Uma segunda declaração da mesma variável é reportada como erro, e a primeira declaração permanece como referência para as verificações seguintes.

## 3. Verificações semânticas

`SemanticAnalyzer` percorre as declarações e os comandos da AST e verifica:

- uso de identificadores declarados em atribuições, expressões e `read`;
- declarações duplicadas;
- igualdade entre o tipo da variável atribuída e o tipo da expressão;
- operandos `int` em operações aritméticas e comparações de ordem (`<`, `<=`, `>` e `>=`);
- operandos `bool` em `&&`, `||` e `!`, e operando `int` em menos unário;
- operandos do mesmo tipo em `==` e `!=`;
- condição `bool` em `if`;
- variáveis declaradas nos comandos `read` e expressões válidas nos comandos `write`.

Os erros semânticos incluem a linha sempre que a AST disponibiliza essa posição. O analisador acumula os erros encontrados e encerra a compilação com código diferente de zero. A semântica de `write` aceita expressões `int` e `bool`, e `read` aceita variáveis de ambos os tipos.

## 4. Integração e execução

`src/main.py` executa lexer, parser e, em seguida, analisador semântico. Se houver erro semântico, cada diagnóstico é impresso e o processo retorna código 1. A AST JSON e a mensagem de conclusão só aparecem quando as três etapas são concluídas sem erros.

O comando para executar a suíte é:

```bash
python run_tests.py
```

O executor preserva os casos léxicos e sintáticos existentes em `minic_tests/` e também procura casos válidos e erros semânticos em `minic_test/`.

## 5. Casos adicionados

Foram adicionados três programas em `minic_test/`:

- `valido_semantico.mc`: declara e usa `int` e `bool`, faz operações aritméticas e relacionais e executa `if`/`write` corretamente;
- `erro_semantico_nao_declarada.mc`: usa uma variável não declarada numa expressão;
- `erro_semantico_tipos.mc`: tenta usar um `bool` em operação aritmética e um `int` como condição de `if`.

Os dois casos inválidos devem ser rejeitados com diagnóstico semântico; o caso válido deve ser aceito.

## 6. Arquivos alterados

- `src/semantic.py`: tabela de símbolos e regras semânticas;
- `src/parser.py`: preserva linhas relevantes da AST para diagnósticos sem alterar a representação JSON;
- `src/main.py`: integra a análise semântica ao fluxo de compilação;
- `run_tests.py`: inclui os casos semânticos e percorre as pastas de teste existentes e novas;
- `README.md`: atualiza escopo, estrutura e instruções de execução.

## 7. Conclusão

O compilador agora rejeita programas lexical e sintaticamente válidos que violem as regras de declaração ou de tipos da MiniC. As etapas anteriores continuam separadas por módulo, e a análise semântica consome a AST produzida pelo parser.
