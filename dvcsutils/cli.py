import os, sys, argparse
from .core import actions, load, detect, find, root
from .repo import Repo


def get_arguments():
    parser = argparse.ArgumentParser(description='Abstract DVCS interface.')
    parser.add_argument('action', metavar='ACTION', choices=actions.keys(), help='action(s) to perform')
    parser.add_argument('parameters', nargs='*', metavar='PARAMETER', help='parameter(s) to pass to action')
    parser.add_argument('-d', '--directory', help='the working directory')
    parser.add_argument('-m', '--message', help='the commit message')
    return parser.parse_args()


def main():
    args = get_arguments()

    if not args.directory:
        args.directory = os.getcwd()

    r = load(directory=args.directory)

    status = 0

    f = getattr(r, args.action)

    if args.action in ('commit',):
        status = f(*args.parameters, message=args.message)
    elif args.action in ('archive', 'export'):
        status = f(args.output_directory)
    elif args.action in ('add', 'rm', 'mv'):
        status = f(*args.parameters)
    else:
        status = f()

    sys.exit(status)
