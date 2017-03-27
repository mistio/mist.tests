import argparse
import types
import sys

from misttests import config

from prepare_env import snake_to_arg, prepare_arg_parser, clean_args

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

    import ipdb;ipdb.set_trace()

    args_to_be_cleaned = sys.argv[1:]
    clean_args(args_to_be_cleaned, cleanup_list)

    if args.gui and args.api:
        raise Exception("You must either provide the gui or the api flag but "
                        "not both. If you provide no flag then the behave will"
                        " be invoked")
    elif args.gui:
        import behave.__main__
        sys.exit(behave.__main__.main(args_to_be_cleaned))
    elif args.api:
        import pytest
        sys.exit(pytest.main(args_to_be_cleaned))
