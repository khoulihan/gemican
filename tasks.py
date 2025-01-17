import os
from pathlib import Path
from shutil import which

from invoke import task

PKG_NAME = "gemican"
PKG_PATH = Path(PKG_NAME)
DOCS_PORT = os.environ.get("DOCS_PORT", 8000)
BIN_DIR = "bin" if os.name != "nt" else "Scripts"
ACTIVE_VENV = os.environ.get("VIRTUAL_ENV", None)
VENV_HOME = Path(os.environ.get("WORKON_HOME", "~/virtualenvs"))
VENV_PATH = Path(ACTIVE_VENV) if ACTIVE_VENV else (VENV_HOME / PKG_NAME)
VENV = str(VENV_PATH.expanduser())
VENV_BIN = Path(VENV) / Path(BIN_DIR)

TOOLS = ["poetry", "pre-commit", "psutil"]
POETRY = which("poetry") if which("poetry") else (VENV_BIN / "poetry")
PRECOMMIT = (
    which("pre-commit") if which("pre-commit") else (VENV_BIN / "pre-commit")
)


@task
def docbuild(c):
    """Build documentation"""
    c.run(f"{VENV_BIN}/sphinx-build -W docs docs/_build")


@task(docbuild)
def docserve(c):
    """Serve docs at http://localhost:$DOCS_PORT/ (default port is 8000)"""
    from livereload import Server

    server = Server()
    server.watch("docs/conf.py", lambda: docbuild(c))
    server.watch("CONTRIBUTING.rst", lambda: docbuild(c))
    server.watch("docs/*.rst", lambda: docbuild(c))
    server.serve(port=DOCS_PORT, root="docs/_build")


@task
def tests(c):
    """Run the test suite"""
    PTY = True if os.name != "nt" else False
    c.run(f"{VENV_BIN}/pytest", pty=PTY)


@task
def black(c, check=False, diff=False):
    """Run Black auto-formatter, optionally with --check or --diff"""
    check_flag, diff_flag = "", ""
    if check:
        check_flag = "--check"
    if diff:
        diff_flag = "--diff"
    c.run(f"{VENV_BIN}/black {check_flag} {diff_flag} {PKG_PATH} tasks.py")


@task
def isort(c, check=False, diff=False):
    check_flag, diff_flag = "", ""
    if check:
        check_flag = "-c"
    if diff:
        diff_flag = "--diff"
    c.run(
        f"{VENV_BIN}/isort {check_flag} {diff_flag} ."
    )


@task
def flake8(c):
    c.run(f"git diff HEAD | {VENV_BIN}/flake8 --diff --max-line-length=88")


@task
def lint(c):
    flake8(c)


@task
def tools(c):
    """Install tools in the virtual environment if not already on PATH"""
    for tool in TOOLS:
        if not which(tool):
            c.run(f"{VENV_BIN}/python -m pip install {tool}")


@task
def precommit(c):
    """Install pre-commit hooks to .git/hooks/pre-commit"""
    c.run(f"{PRECOMMIT} install")


@task
def setup(c):
    c.run(f"{VENV_BIN}/python -m pip install -U pip")
    tools(c)
    c.run(f"{POETRY} install")
    precommit(c)


@task
def update_functional_tests(c):
    """Update the generated functional test output"""
    c.run(
        (
            f"bash -c 'LC_ALL=en_US.utf8 gemican"
            f" -o {PKG_PATH}/tests/output/custom/"
            f" -s samples/gemican.conf.py samples/content/'"
        )
    )
    c.run(
        (
            f"bash -c 'LC_ALL=fr_FR.utf8 gemican"
            f" -o {PKG_PATH}/tests/output/custom_locale/"
            f" -s samples/gemican.conf_FR.py samples/content/'"
        )
    )
    c.run(
        (
            f"bash -c 'LC_ALL=en_US.utf8 gemican"
            f" -o {PKG_PATH}/tests/output/basic/ samples/content/'"
        )
    )
