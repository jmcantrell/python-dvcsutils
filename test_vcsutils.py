#!/usr/bin/env python

import os, shutil, unittest
import vcsutils


def resource(name):
    return os.path.join(os.path.dirname(__file__), name)


class MainTestCase(unittest.TestCase):

    def setUp(self):
        self.init_repos()

    def init_repos(self):
        self.directory = resource('repos')
        if os.path.isdir(self.directory):
            shutil.rmtree(self.directory)
        self.repos = []
        os.makedirs(self.directory)
        for t, cls in vcsutils.vcs_types.items():
            r = vcsutils.vcs_types[t](directory=os.path.join(self.directory, t))
            self.repos.append(r)
            r.init()


class ModuleTestCase(MainTestCase):

    def test_clone(self):
        for r in self.repos:
            cls = type(r)
            rc = cls(directory=r.directory+'-clone')
            rc.clone(r.directory)
            self.assertTrue(type(rc).detect(rc.directory))


class CommandLineTestCase(MainTestCase):
    pass


if __name__ == '__main__':
    unittest.main()
