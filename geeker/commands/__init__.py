# -*- coding: utf-8 -*-

import click
from geeker import __Version__, __UpdateTime__, __all__, __Description__


@click.command(name='v')
def version():
    """
    Current version.
    """

    click.echo(__Version__)


@click.command(name='t')
def time_stamp():
    """
    The last update time.
    """

    click.echo(__UpdateTime__)


@click.command(name='a')
def about():
    """
    About problems .
    """
    click.echo(__Description__)


@click.command(name='m')
@click.option("--module", prompt="input module name")  # prompt功能:直接弹出一行，让用户输入
def how_use(module):
    """
    How to use some module.
    """
    tmp = 'https://github.com/4379711/functools_lyl#' + str(module).lower().replace(" ", '-')
    click.echo('You can find answer in this url.')
    click.echo(tmp)


@click.command(name='M')
def list_module():
    """
    ALL modules .
    """
    tmp = (i for i in __all__ if not i.startswith('__'))
    for module in tmp:
        click.echo(module)


@click.group()
def base_command():
    pass


# 添加到组
base_command.add_command(how_use)
base_command.add_command(list_module)
base_command.add_command(version)
base_command.add_command(time_stamp)
base_command.add_command(about)

if __name__ == '__main__':
    base_command()
