import os

dvcs_types = {}
commands = ['commands']


def detect(directory):
    for tcls in dvcs_types.values():
        if tcls.detect(directory):
            return tcls


def root(directory):
    while directory != os.path.sep:
        if detect(directory):
            return directory
        directory = os.path.dirname(directory)


def load(directory, dvcs_type=None):
    repo_cls = detect(directory)
    if repo_cls:
        return repo_cls(directory)
    if dvcs_type:
        return dvcs_types[dvcs_type](directory)


def find(directory):
    if detect(directory):
        yield load(directory)
    for root, dirs, files in os.walk(directory):
        for d in dirs:
            p = os.path.join(root, d)
            if detect(p):
                yield load(p)
