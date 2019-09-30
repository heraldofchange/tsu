# Copyright (c) 2019, Cswl Coldwind <cswl1337@gmail.com
# This software is licensed under the MIT Liscense.
# https://github.com/cswl/tsu/blob/v3.x/LICENSE-MIT

import subprocess
import re

from pathlib import Path
from . import consts

from decorator import getfullargspec
from .conlog import Conlog

print(getfullargspec(Conlog.fn))


@Conlog.module
class exec:
    @Conlog.fn
    def ver_cmp(console, su):
        reg = su['verstring']
        checkver = [su['path']] + su['veropt']
        try:
            ver = subprocess.check_output(checkver).decode('utf-8')
            console.debug(f"{ver_cmp}")
            if re.match(reg, ver):
                return True
            else:
                return "VERERR"
        except PermissionError as e:
            return False


def linux_execve(cmd, args, env=None):
    exec = [cmd] + args
    subprocess.run(exec, env=env)


def magisk_call(console, shell, env=None):
    argv = ["su", "-s", shell]
    console.debug(argv)
    linux_execve(consts.MAGISK_BINARY, argv)


def su_call(console, su, shell, env):
    argv = ["su", "-s", shell]
    console.debug(argv)
    linux_execve(su, argv)


def su_params(shell, preserve=True):
    return f"-s {shell} --preserve-environment"
