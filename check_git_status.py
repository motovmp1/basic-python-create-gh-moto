import subprocess
import sys
from pathlib import Path


PASTA_PROJETO = Path(
    r"C:\Users\vinicius.pinho\Documents\basic_github_account"
)


def verificar_git(pasta: Path) -> int:
    if not pasta.exists():
        print(f"ERRO: a pasta nao existe: {pasta}")
        return 2

    resultado = subprocess.run(
        [
            "git",
            "-C",
            str(pasta),
            "status",
            "--porcelain",
            "--untracked-files=all",
        ],
        capture_output=True,
        text=True,
    )

    if resultado.returncode != 0:
        print(f"ERRO: a pasta nao e um repositorio Git: {pasta}")
        print(resultado.stderr.strip())
        return 2

    alteracoes = resultado.stdout.strip()

    print(f"Pasta verificada: {pasta}")

    if not alteracoes:
        print("STATUS VERDE: pasta limpa.")
        print("O teste pode comecar.")
        return 0

    print("STATUS VERMELHO: existem alteracoes locais.")
    print()
    print("Arquivos encontrados:")
    print(alteracoes)
    print()
    print("O teste nao deve comecar.")
    return 1


if __name__ == "__main__":
    codigo = verificar_git(PASTA_PROJETO)
    sys.exit(codigo)