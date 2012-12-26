import os, argparse
from .core import load, find, commands


def parse_args():
    parser = argparse.ArgumentParser(description='Abstract DVCS interface.')
    parser.add_argument('command', metavar='command', choices=commands, help='command(s) to perform')
    parser.add_argument('parameters', nargs='*', metavar='parameter', help='parameter(s) to pass to command')
    parser.add_argument('-d', '--directory', help='the working directory')
    parser.add_argument('-m', '--message', help='the commit message')
    parser.add_argument('-r', '--recursive', action='store_true', help='use all repos under directory')
    return parser.parse_args()


def process(r, args):
    if args.command == 'commands':
        for c in sorted(commands):
            print(c)
        return
    f = getattr(r, args.command)
    if args.command == 'commit':
        f(*args.parameters, message=args.message)
    elif args.command in ('archive', 'export'):
        f(args.output_directory)
    elif args.command in ('add', 'remove', 'move'):
        f(*args.parameters)
    else:
        f()


def main():
    args = parse_args()
    # If no directory was given, use CWD
    if not args.directory:
        args.directory = os.getcwd()
    if args.recursive:
        for r in find(args.directory):
            print(r.directory)
            process(r, args)
            print('')
    else:
        process(load(args.directory), args)
