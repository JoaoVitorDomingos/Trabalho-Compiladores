from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).parent
TESTS = ROOT / "minic_tests"

valid = sorted(TESTS.glob("valido_*.mc"))
invalid_lex = TESTS / "erro_lexico.mc"
invalid_syn = sorted(TESTS.glob("erro_sintatico*.mc"))

failures = []

for path in valid:
    result = subprocess.run([sys.executable, str(ROOT / "src" / "main.py"), str(path)], capture_output=True, text=True)
    if result.returncode != 0 or "Análise concluída com sucesso." not in result.stdout:
        failures.append(f"válido: {path.name}\n{result.stdout}{result.stderr}")

result = subprocess.run([sys.executable, str(ROOT / "src" / "main.py"), str(invalid_lex)], capture_output=True, text=True)
if result.returncode == 0 or "Erro léxico" not in result.stdout:
    failures.append(f"léxico: {invalid_lex.name}\n{result.stdout}{result.stderr}")

for path in invalid_syn:
    result = subprocess.run([sys.executable, str(ROOT / "src" / "main.py"), str(path)], capture_output=True, text=True)
    if result.returncode == 0 or "Erro sintático" not in result.stdout:
        failures.append(f"sintático: {path.name}\n{result.stdout}{result.stderr}")

if failures:
    print("TESTES COM FALHA")
    print("\n".join(failures))
    raise SystemExit(1)

print(f"Todos os testes passaram: {len(valid)} válidos, 1 léxico e {len(invalid_syn)} sintáticos.")
