#!/usr/bin/env python
#coding: UTF-8
"""Generate the breakpad symbol file and place it in the directory structure
required by breakpad `minidump_stackwalk` tool.
"""

from __future__ import print_function
import os
from os.path import abspath, basename, exists, dirname, join
import re
import sys
import subprocess

BP_SYMBOLS_FILE = 'testbp.sym'


def call(*a, **kw):
    kw.setdefault('shell', True)
    subprocess.check_call(*a, **kw)


def get_command_output(cmd, **kw):
    shell = not isinstance(cmd, list)
    return subprocess.check_output(cmd, shell=shell, **kw)

# mkdir -p ./symbols/testbp/${symbol_id}/
# mv ${BP_SYMBOLS_FILE} ./symbols/testbp/${symbol_id}/


def main():
    seafile_src_dir = dirname(abspath(dirname(__file__)))
    os.chdir(seafile_src_dir)
    seaf_daemon = join('daemon', 'seaf-daemon.exe' if os.name == 'nt' else
                       'seaf-daemon')
    symbols = get_command_output('dump_syms {}'.format(seaf_daemon))
    symbol_id = symbols.splitlines()[0].split()[3]
    symbol_dir = join('symbols', 'seaf-daemon', symbol_id)
    if not exists(symbol_dir):
        os.makedirs(symbol_dir)
    symbol_file = join(symbol_dir, 'seaf-daemon.sym')
    with open(symbol_file, 'w') as fp:
        print('symbols written to {}'.format(symbol_file))
        fp.write(symbols)


if __name__ == '__main__':
    main()
