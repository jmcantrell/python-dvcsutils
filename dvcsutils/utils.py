import os, shlex
from pipes import quote
from contextlib import contextmanager
from subprocess import PIPE, Popen


class AutoRegister(type):

    def __new__(mcs, name, bases, classdict):
        new_cls = type.__new__(mcs, name, bases, classdict)
        for b in bases:
            if hasattr(b, 'register_subclass'):
                b.register_subclass(new_cls)
        return new_cls


@contextmanager
def cd(path):
    prev_cwd = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(prev_cwd)


def in_directory(f, directory=None):
    def new_f(self, *args, **kwargs):
        d = directory or kwargs.get('directory') or vars(self).get('directory')
        with cd(d or os.getcwd()):
            return f(self, *args, **kwargs)
    new_f.func_name = f.func_name
    return new_f


def split_command(cmd):
    if isinstance(cmd, (list, tuple)):
        return cmd
    return shlex.split(cmd)


def run(cmd, **kwargs):
    p = Popen(split_command(cmd), **kwargs)
    o, e = p.communicate()
    return p.returncode == 0


def get(cmd, **kwargs):
    return lines(cmd, **kwargs)[0]


def lines(cmd, **kwargs):
    kwargs['stdout'] = PIPE
    return run(cmd, **kwargs)[1].split(os.linesep)


def quote(*args):
    return ' '.join([quote(a) for a in args])
