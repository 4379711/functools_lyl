# -*- coding: utf-8 -*-
# @Time    : 2019/11/12 14:14
# @Author  : Liu Yalong
# @File    : __main__.py
import os
import sys
import gc

if not __package__:
    path = os.path.join(os.path.dirname(__file__), os.pardir)
    sys.path.insert(0, path)
from geeker.commands import base_command

base_command()
gc.collect()
