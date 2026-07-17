import subprocess
import sys
from pathlib import Path


PASTA_PROJETO = Path(
    r"C:\Users\vinicius.pinho\Documents\basic_github_account"
)


def executar_git(*argumentos):
    return subprocess.run(
        ["git", "-C", str(PASTA_PROJETO), *argumentos],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def verificar_main():
    print(f"Pasta: {PASTA_PROJETO}")

    if not PASTA_PROJETO.exists():
        print("ERRO: a pasta nao existe.")
        return 2

    repositorio = executar_git("rev-parse", "--is-inside-work-tree")

    if repositorio.returncode != 0:
        print("ERRO: a pasta nao e um repositorio Git.")
        return 2

    print("Consultando a main mais recente no GitHub...")

    fetch = executar_git("fetch", "origin", "main")

    if fetch.returncode != 0:
        print("ERRO: nao foi possivel consultar o GitHub.")
        print(fetch.stderr.strip())
        return 2

    branch = executar_git("branch", "--show-current").stdout.strip()
    commit_local = executar_git("rev-parse", "--short", "HEAD").stdout.strip()
    commit_main = executar_git(
        "rev-parse", "--short", "origin/main"
    ).stdout.strip()

    print(f"Branch atual: {branch}")
    print(f"Commit atual: {commit_local}")
    print(f"Main GitHub:  {commit_main}")

    status = executar_git(
        "status",
        "--porcelain",
        "--untracked-files=all",
    )

    comparar = executar_git(
        "diff",
        "--quiet",
        "origin/main",
        "--",
    )

    alteracoes = status.stdout.strip()

    if comparar.returncode == 0 and not alteracoes:
        print()
        print("STATUS VERDE")
        print("O conteudo da pasta e igual a main mais recente.")
        print("O teste pode comecar.")
        return 0

    if comparar.returncode not in (0, 1):
        print("ERRO: nao foi possivel comparar os arquivos.")
        print(comparar.stderr.strip())
        return 2

    print()
    print("STATUS VERMELHO")
    print("O conteudo da pasta NAO e igual a main mais recente.")
    print("O teste nao deve comecar.")

    commits = executar_git(
        "log",
        "--oneline",
        "--left-right",
        "HEAD...origin/main",
    ).stdout.strip()

    if commits:
        print()
        print("Commits diferentes:")
        print(commits)

    if alteracoes:
        print()
        print("Alteracoes locais:")
        print(alteracoes)

    return 1


if __name__ == "__main__":
    sys.exit(verificar_main())