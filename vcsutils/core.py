vcs_types = {}
actions = {}

import os
from .repo import Repo


def detect(directory):
    for tclass in vcs_types.values():
        if tclass.detect(directory):
            return tclass


def load(directory, vcs_type=None):
    repo_cls = detect(directory)
    if repo_cls:
        return repo_cls(directory=directory)
    if vcs_type:
        return vcs_types[vcs_type](directory=directory)


def find(directory):
    if Repo.detect(directory):
        yield load(directory)
    for root, dirs, files in os.walk(directory):
        for d in dirs:
            p = os.path.join(root, d)
            if detect(p):
                yield load(p)


def root(directory):
    while directory != os.path.sep:
        if detect(directory):
            return directory
        directory = os.path.dirname(directory)
