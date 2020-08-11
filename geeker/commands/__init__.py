# -*- coding: utf-8 -*-

import click
from geeker import __Version__, readme, __UpdateTime__


@click.command(name='-v')
def version():
    """
    查看当前版本
    """

    click.echo(__Version__)


@click.command(name='-t')
def time_stamp():
    """
    查看最后更新时间
    """

    click.echo(__UpdateTime__)


@click.command(name='-u')
@click.option("-m", prompt="请输入模块名")  # prompt直接弹出一行，让用户输入
def how_use(module):
    """
    查看某模块的使用方式

    """

    all_modules_dict = readme()
    tmp_ = all_modules_dict.get(module, None)
    if not tmp_:
        click.secho(f"ERROR: \tcan't find module <{module}>!", color='red')
    else:
        click.echo(tmp_)


@click.command(name='-m')
def list_module():
    """
    查看所有的模块
    """

    all_modules_dict = readme()
    modules = list(all_modules_dict.keys())
    click.echo(modules)


# 分组功能，将多个命令分组
@click.group()
def base_command():
    pass


# 添加到组
base_command.add_command(how_use)
base_command.add_command(list_module)
base_command.add_command(version)

if __name__ == '__main__':
    base_command()
