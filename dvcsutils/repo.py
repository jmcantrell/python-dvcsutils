import os
from .core import actions, dvcs_types
from .utils import in_directory, quote, lines, get, run, AutoRegister


def action(f):
    actions[f.func_name] = f
    return f


class Repo:  # {{{1

    __metaclass__ = AutoRegister

    dvcs_type = None

    def __init__(self, directory=None):
        self.directory = directory or os.getcwd()

    def command(self, cmd):
        return ' '.join([self.dvcs_type, cmd])

    def lines(self, cmd, **kwargs):
        return lines(self.command(cmd), **kwargs)

    def get(self, cmd, **kwargs):
        return get(self.command(cmd), **kwargs)

    def run(self, cmd, **kwargs):
        return run(self.command(cmd), **kwargs)

    @property
    def name(self):
        return os.path.basename(self.directory)

    @classmethod
    def detect(cls, directory):
        if not cls.dvcs_type:
            return False
        return os.path.isdir(os.path.join(directory, '.'+cls.dvcs_type))

    @classmethod
    def register_subclass(klass, cls):
        dvcs_types[cls.dvcs_type] = cls

    @in_directory
    def get_url(self):
        raise NotImplementedError

    @in_directory
    def get_latest(self):
        return NotImplementedError

    def get_origin(self):
        return '+'.join([self.dvcs_type, self.get_url()])

    # Internal actions {{{2
    # Any Repo class should override these

    def _url(self):
        raise NotImplementedError

    def _latest(self):
        raise NotImplementedError

    def _init(self):
        raise NotImplementedError

    def _clone(self, url):
        raise NotImplementedError

    def _add(self, *files):
        raise NotImplementedError

    def _rm(self, *files):
        raise NotImplementedError

    def _mv(self, *files):
        raise NotImplementedError

    def _diff(self):
        raise NotImplementedError

    def _pull(self):
        raise NotImplementedError

    def _push(self):
        raise NotImplementedError

    def _commit(self, message=None):
        raise NotImplementedError

    def _status(self):
        raise NotImplementedError

    def _export(self, directory):
        raise NotImplementedError

    def _archive(self, directory):
        raise NotImplementedError

    def _check(self):
        raise NotImplementedError

    def _clean(self):
        raise NotImplementedError

    def _purge(self):
        raise NotImplementedError

    def _reset(self):
        raise NotImplementedError

    # External actions {{{2
    # Intended to be the API
    # Exposed to the CLI interface

    @action
    def actions(self):
        for name in sorted(actions.keys()):
            print(name)

    @action
    def init(self):
        return self._init()

    @action
    def clone(self, url):
        return self._clone(url)

    @action
    def origin(self):
        print(self.get_origin())

    @action
    def url(self):
        print(self.get_url())

    @action
    def latest(self):
        print(self.get_latest())

    @action
    @in_directory
    def add(self, *files):
        return self._add(*files)

    @action
    @in_directory
    def rm(self, *files):
        return self._rm(*files)

    @action
    @in_directory
    def mv(self, *files):
        return self._mv(*files)

    @action
    @in_directory
    def diff(self):
        return self._diff()

    @action
    @in_directory
    def pull(self):
        return self._pull()

    @action
    @in_directory
    def push(self):
        return self._push()

    @action
    @in_directory
    def commit(self, message=None):
        return self._commit(message)

    @action
    @in_directory
    def status(self):
        return self._status()

    @action
    @in_directory
    def export(self, directory):
        return self._export(directory)

    @action
    @in_directory
    def archive(self, directory):
        return self._archive(directory)

    @action
    @in_directory
    def check(self):
        return self._check()

    @action
    @in_directory
    def clean(self):
        return self._clean()

    @action
    @in_directory
    def purge(self):
        return self._purge()

    @action
    @in_directory
    def reset(self):
        return self._reset()


class RepoGit(Repo):  # {{{1

    dvcs_type = 'git'

    def _url(self):
        return self.get('config remote.origin.url')

    def _latest(self):
        return self.get('rev-parse HEAD')

    def _init(self):
        return self.run('init {}'.format(quote(self.directory)))

    def _clone(self, url):
        return self.run('clone {}'.format(quote(url, self.directory)))

    def _status(self):
        return self.run('status')

    def _add(self, *files):
        return self.run('add {}'.format(quote(*files)))

    def _diff(self):
        return self.run('diff')

    def _mv(self, *files):
        return self.run('mv {}'.format(quote(*files)))

    def _rm(self, *files):
        return self.run('rm -f {}'.format(quote(*files)))

    def _pull(self):
        return self.run('pull --recurse-submodules')

    def _push(self):
        return self.run('push')

    def _commit(self, message=None):
        if message:
            return self.run('commit -a -v -m {}'.format(quote(message)))
        else:
            return self.run('commit -a -v')

    def _check(self):
        return self.run('fsck') and self.run('gc')

    def _clean(self):
        return self.run('clean -fd')

    def _purge(self):
        return self.run('clean -fdx')

    def _reset(self):
        return self.run('reset --hard HEAD')

    def _export(self, directory):
        return self.run('checkout-index -a -f --prefix={}/'.format(quote(directory)))

    def _archive(self, directory):
        return self.run(
                'archive --format=zip --output={}.zip --prefix={}/ HEAD'.format(
                    quote(os.path.join(directory, self.name)),
                    quote(self.name)
                    )
                )


class RepoMercurial(Repo):  # {{{1

    dvcs_type = 'hg'

    def _url(self):
        return self.get('paths default')

    def _latest(self):
        return self.get('revno')

    def _init(self):
        return self.run('init {}'.format(quote(self.directory)))

    def _clone(self, url):
        return self.run('clone {}'.format(quote(url, self.directory)))

    def _status(self):
        return self.run('status')

    def _add(self, *files):
        return self.run('add {}'.format(quote(*files)))

    def _mv(self, *files):
        return self.run('mv {}'.format(quote(*files)))

    def _rm(self, *files):
        return self.run('rm -f {}'.format(quote(*files)))

    def _diff(self):
        return self.run('diff')

    def _pull(self):
        return self.run('pull -u')

    def _push(self):
        return self.run('push')

    def _commit(self, message=None):
        if message:
            return self.run('commit -v -m {}'.format(quote(message)))
        else:
            return self.run('commit -v')

    def _check(self):
        return self.run('verify')

    def _clean(self):
        return self.run('purge -v')

    def _purge(self):
        return self.run('purge --all')

    def _reset(self):
        return self.run('revert -a')

    def _export(self, directory):
        return self.run('archive {}'.format(quote(directory)))

    def _archive(self, directory):
        return self.run(
                'archive -p {} -t zip {}.zip'.format(
                    quote(self.name),
                    quote(self.name)
                    )
                )


class RepoBazaar(Repo):  # {{{1

    dvcs_type = 'bzr'

    def get_info(self, key):
        for line in self.lines('info'):
            if key+': ' in line:
                return line.split(': ')[1]

    def _url(self):
        return self.get_info('parent branch')

    def _latest(self):
        return self.get('id -i')

    def _init(self):
        return self.run('init {}'.format(quote(self.directory)))

    def _clone(self, url):
        return self.run('checkout {}'.format(quote(url, self.directory)))

    def _add(self, *files):
        return self.run('add {}'.format(quote(*files)))

    def _mv(self, *files):
        return self.run('mv {}'.format(quote(*files)))

    def _rm(self, *files):
        return self.run('remove --force {}'.format(quote(*files)))

    def _diff(self):
        return self.run('diff')

    def _pull(self):
        return self.run('update')

    def _push(self):
        return self.run('commit')

    def _status(self):
        return self.run('status')

    def _commit(self, message=None):
        if message:
            return self.run('commit --local -m {}'.format(quote(message)))
        else:
            return self.run('commit --local')

    def _check(self):
        return self.run('check -v')

    def _clean(self):
        return self.run('clean-tree -v --force --detritus --unknown')

    def _purge(self):
        return self.run('clean-tree -v --force --detritus --unknown --ignored')

    def _reset(self):
        return self.run('revert -v')

    def _export(self, directory):
        return self.run('export -v --root={}'.format(quote(self.name)))

    def _archive(self, directory):
        return self.run('export -v --root={} {}.zip'.format(quote(self.name), quote(self.name)))
