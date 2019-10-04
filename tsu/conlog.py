# Copyright (c) 2019, Cswl Coldwind <cswl1337@gmail.com
# This software is licensed under the MIT Liscense.
# https://github.com/cswl/tsu/blob/v3.x/LICENSE-MIT

import logging
import subprocess
import inspect

import wrapt
import re
import functools

from colored import fore, back, style


### Dummy function to debug Conlog itself
def _cdebug(fstr, *args):
    enabled = False
    if enabled:
        expstr = _expr_debug(fstr, patt="_cdebug")
        print(expstr)

# Uses ugly hack to support f"{expr=}" in 3.7+\
def _expr_debug(fstr, patt="console.debug"):
    py_version = 37

    if py_version < 38:
        # Get 2 stack frames back
        frame = inspect.currentframe()
        callerframe = frame.f_back.f_back
        try:
            context = inspect.getframeinfo(callerframe ).code_context
            caller_lines = ''.join([line.strip() for line in context])
            #print(caller_lines)
            m = re.search( re.compile(patt + r'\s*\((.+?)\)$'), caller_lines)
            rexpr = r"(\{.*?\=\})"
            a = re.findall(rexpr, fstr)
            ae = [re.sub(r"\{|\}|\=", "", e) for e in a]
            if m:
                caller_lines = m.group(1)
                expstr = [
                    f"{fore.LIGHT_BLUE}{style.BOLD}{e}{style.RESET}= " +
                    str(eval(e, callerframe.f_globals, callerframe.f_locals))
                    for e in ae
                ]
                repl = dict(zip(a, expstr))
                ostr = re.sub(rexpr,
                              lambda mx: repl.get(mx.group(), mx.group()),
                              fstr)
                return ostr

            else:
                return fstr
                pass
        finally:

            del frame
            del callerframe

"""
 Conlog : A console.log for Python

 console = Conlog(__name, enabled=True)

 @conlog.fn
 def cli(console) :
    console.log("Hello world");

 Then you import collections of functions.
 Only collections labelled as
 @Conlog.module works.. it means they support the conlog protocol.

"""
class Conlog():
    CRITICAL = 50
    ERROR = 40
    WARNING = 30
    INFO = 20
    DEBUG = 10
    NONE = 0
    
    """The Conlog.fn decorator."""
    class fn:
        def __init__(self, f):
            _cdebug("static:fn::Init {f=}")
            # Plain function as argument to be decorated
            self.func = f
            self.cache = False

        def __get__(self, instance, owner):
            self.instance_ = instance
            _cdebug("static:fn::Get {self.instance_=} ")
            if not self.cache:
                self.__conlog_console = self.instance_.__conlog_console__
                self.__conlog_impl__ = True
                self.cache = True
            return self.__call__

        def __call__(self, *args, **kwargs):
            """Invoked on every call of any decorated method"""
            self.__conlog_impl__ = True
            # set attribute on instance
            name = self.func.__name__
            instance = self.instance_
            console = self.__conlog_console
            console.debug_func_set(self.func)
            _cdebug(
                "static::fn::ProxyCall {name=} {instance=}   {args=} {kwargs=}"
            )
            return self.func(self.instance_, console, *args, **kwargs)

    class Console:
        def __init__(self, module, logger):
            self.logger = logger
            self.module = module
            #_cdebug("Console", logger, module)

        def debug_func_set(self, func):
            self.__current_func  = func

        def debug(self, msg):
            expr_msg = _expr_debug(msg)
            func_name = getattr(self.__current_func, '__name__', "func")
            format = f"{fore.MAGENTA_3A}{self.module}:{func_name}{expr_msg}"
            print(format)

    def __init__(
            self,
            name,
            level=100,
            enabled=True,
    ):
        self.enabled = enabled
        self.level = level
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.sh = logging.StreamHandler()
        self.logger.addHandler(self.sh)

    @classmethod
    def module(cls, target_cls):
        @wrapt.decorator
        def wrapper(wrapped, instance, args, kwargs):
            _cdebug("module::  {wrapped=} {instance=}")
            wrapped.__conlog_impl__ = True
            return wrapped()

        return wrapper

    def impl(self, cls, level, enabled):
        _cdebug(" impl::  {cls=}, {level=}, {enabled=}")
        instance = cls()
        instance.__conlog_console__ = Conlog.Console(cls.__name__, self.logger)
        _cdebug("impl -> proxy", cls)
        return instance
