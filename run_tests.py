from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).parent
TEST_DIRS = [ROOT / "minic_tests", ROOT / "minic_test"]
all_tests = [path for directory in TEST_DIRS if directory.exists() for path in directory.glob("*.mc")]
valid = sorted(path for path in all_tests if path.name.startswith("valido_"))
invalid_lex = [path for path in all_tests if path.name == "erro_lexico.mc"]
invalid_syn = sorted(path for path in all_tests if path.name.startswith("erro_sintatico"))
invalid_sem = sorted(path for path in all_tests if path.name.startswith("erro_semantico"))

failures = []

for path in valid:
    result = subprocess.run([sys.executable, str(ROOT / "src" / "main.py"), str(path)], capture_output=True, text=True)
    if result.returncode != 0 or "concluída com sucesso." not in result.stdout:
        failures.append(f"válido: {path.name}\n{result.stdout}{result.stderr}")

for path in invalid_lex:
    result = subprocess.run([sys.executable, str(ROOT / "src" / "main.py"), str(path)], capture_output=True, text=True)
    if result.returncode == 0 or "Erro léxico" not in result.stdout:
        failures.append(f"léxico: {path.name}\n{result.stdout}{result.stderr}")

for path in invalid_syn:
    result = subprocess.run([sys.executable, str(ROOT / "src" / "main.py"), str(path)], capture_output=True, text=True)
    if result.returncode == 0 or "Erro sintático" not in result.stdout:
        failures.append(f"sintático: {path.name}\n{result.stdout}{result.stderr}")

for path in invalid_sem:
    result = subprocess.run([sys.executable, str(ROOT / "src" / "main.py"), str(path)], capture_output=True, text=True)
    if result.returncode == 0 or "Erro semântico" not in result.stdout:
        failures.append(f"semântico: {path.name}\n{result.stdout}{result.stderr}")

if failures:
    print("TESTES COM FALHA")
    print("\n".join(failures))
    raise SystemExit(1)

print(f"Todos os testes passaram: {len(valid)} válidos, {len(invalid_lex)} léxicos, {len(invalid_syn)} sintáticos e {len(invalid_sem)} semânticos.")
