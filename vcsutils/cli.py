import os, sys, argparse
from .core import load, detect, find, root
from .repo import Repo


def get_arguments():
    parser = argparse.ArgumentParser(description='Abstract VCS interface.')
    parser.add_argument('actions', nargs='*', choices=Repo.get_actions(), help='action(s) to perform')
    parser.add_argument('-D', '--directory', help='the working directory')
    parser.add_argument('-d', '--output-directory', help='the output directory')
    parser.add_argument('-m', '--message', help='the commit message')
    return parser.parse_args()


def main():
    args = get_arguments()
    if not args.directory:
        args.directory = os.getcwd()
    if not args.output_directory:
        args.output_directory = os.path.join(os.getcwd(), os.path.basename(args.directory))
    r = load(directory=args.directory)
    status = 0
    for action in args.actions:
        f = getattr(r, action)
        if action == 'commit':
            status = f(args.message)
        elif action in ('archive', 'export'):
            status = f(args.output_directory)
        else:
            status = f()
    sys.exit(status)
