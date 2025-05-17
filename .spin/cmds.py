import importlib
import sys
import textwrap

import click
from spin.cmds.util import run


@click.command()
@click.argument("pytest_args", nargs=-1)
@click.option(
    "-c",
    "--coverage",
    is_flag=True,
    help="Generate a coverage report of executed tests.",
)
def test(pytest_args, coverage=False):
    """🔧 Run tests"""
    if not importlib.util.find_spec("lazy_loader"):
        click.secho(
            textwrap.dedent("""\
              ERROR: The package is not installed.

              Please do an editable install:

                pip install -e .[test]

              prior to running the tests."""),
            fg="red",
        )
        sys.exit(1)

    if coverage:
        pytest_args = ("--cov=lazy_loader", *pytest_args)
    run([sys.executable, "-m", "pytest", *list(pytest_args)])
