import sys

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
    if coverage:
        pytest_args = ("--cov=lazy_loader", *pytest_args)
    run([sys.executable, "-m", "pytest", *list(pytest_args)])
