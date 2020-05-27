# -*- coding: utf-8 -*-

import os
import sys

if not __package__:
    path = os.path.join(os.path.dirname(__file__), os.pardir)
    sys.path.insert(0, path)
from geeker.cmdline import base_command  # noqa

if __name__ == '__main__':
    base_command()
