# Copyright (c) 2019, Cswl Coldwind <cswl1337@gmail.com
# This software is licensed under the MIT Liscense.
# https://github.com/cswl/tsu/blob/v3.x/LICENSE-MIT

import logging
import subprocess

from decorator import decorator
import functools
"""
 Conlog : A console.log for Python

conlog = Conlog(__name, enabled=True)

 @conlog.fn
 def cli(console) :
    console.log("Hello world");

"""


class Conlog():
    CRITICAL = 50
    ERROR = 40
    WARNING = 30
    INFO = 20
    DEBUG = 10
    NONE = 0

    def __init__(self, level, enabled=True, ):
        self.enabled = enabled
        self.level = level
        self.logger = logging.getLogger(module)
        self.logger.setLevel(level)
        self.sh = logging.StreamHandler()
        self.logger.addHandler(self.sh)

    @decorator
    def module(self, cls, *args, **kwargs):
        print(args)
        cls.console = self.console

    @decorator
    def fn(self, func, *args, **kwargs):
        console = self
        console.debug = functools.partial(self.__debug, func.__name__)
        val = func(console, *args, **kwargs)
        return val



    def __debug(self, func, msg):
        format = f"{self.module}:{func}  {msg}"
        self.logger.debug(format)
