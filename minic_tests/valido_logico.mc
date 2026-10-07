program Logico {
    int a, b;
    bool resultado;
    read(a, b);
    resultado = !(a < b) || a == b && true;
    write(resultado, -a, (a + b) / 2);
}
