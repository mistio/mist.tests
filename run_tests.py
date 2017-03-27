import argparse
import types
import sys

from misttests import config

from prepare_env import snake_to_arg, prepare_arg_parser, arg_to_snake


def get_pytest_args(args_given):
    pytest_args = []
    pytest_args.append('-s')
    api_test_path = 'tests/misttests/api/core/' + args_given[0].strip('-') + '.py'
    pytest_args.append(api_test_path)
    return pytest_args


def validate_args(args_to_be_cleaned):
    for arg in args_to_be_cleaned:
        arg = arg.strip('-')
        if arg not in ['clouds, machines, keys, scripts, images, api_token',
                       'tunnels', 'schedules']:
            raise Exception("Api tests can run on the following resources: clouds, machines, keys,"
                            "scripts, images, api_token")


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
                        "not both.")
    elif args.gui:
        import behave.__main__
        sys.exit(behave.__main__.main(args_to_be_cleaned))
    elif args.api:
        validate_args(args_to_be_cleaned)
        import ipdb;ipdb.set_trace()
        pytest_args = get_pytest_args(args_to_be_cleaned)
        import pytest
        sys.exit(pytest.main(pytest_args))
    else:
        raise Exception("Seriously now? WTF are you doing?")


# API - run multiple tests
# API - run entire suite
# API + UI - run everything if no flag
# cleanup
# UI
