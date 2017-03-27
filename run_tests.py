import argparse
import types
import sys

from misttests import config

from prepare_env import snake_to_arg, prepare_arg_parser


def arg_index(arg_list, arg):
    for i in range(len(arg_list)):
        if arg_list[i].startswith(arg):
            return i
    raise ValueError


def clean_args(arg_list, args_to_be_removed):
    if len(arg_list) == 0 or len(args_to_be_removed) == 0:
        return
    next_arg_to_clean = args_to_be_removed.pop()
    try:
        while True:
            index = arg_index(arg_list, next_arg_to_clean)
            del arg_list[index]
            while index < len(arg_list) and not arg_list[index].startswith('-'):
                del arg_list[index]
    except ValueError:
        pass
    clean_args(arg_list, args_to_be_removed)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='')

    cleanup_list = []
    for attr in dir(config):
        if not isinstance(attr, types.FunctionType):
            if isinstance(attr, basestring):
                if attr.startswith('__') or attr.islower():
                    continue

            arg = snake_to_arg(attr)
            prepare_arg_parser(parser, cleanup_list, arg, default=None)

    prepare_arg_parser(parser, cleanup_list, '--gui', action='store_true')
    prepare_arg_parser(parser, cleanup_list, '--api', action='store_true')

    args = parser.parse_known_args()[0]

    args_to_be_cleaned = sys.argv[1:]
    clean_args(args_to_be_cleaned, cleanup_list)

    if args.gui and args.api:
        raise Exception("You must either provide the gui or the api flag but "
                        "not both")
    elif args.gui:
        import behave.__main__
        sys.exit(behave.__main__.main(args_to_be_cleaned))
    elif args.api:
        import ipdb;ipdb.set_trace()
        args_to_be_cleaned.append('-s')
        args_to_be_cleaned.append('tests/misttests/api/core/clouds.py')
        import pytest
        # here check args to be cleaned...
        sys.exit(pytest.main(args_to_be_cleaned))
