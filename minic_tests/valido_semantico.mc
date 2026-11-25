program SemanticoValido {
    int quantidade;
    bool positivo;
    quantidade = 3 + 4 * 2;
    positivo = quantidade > 0;
    if (positivo) {
        write(quantidade, positivo);
    }
}
