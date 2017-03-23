import sys
import types
import logging
import argparse

from misttests import config

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def prepare_arg_parser(parser, arg_list, arg_name, *args, **kwargs):
    parser.add_argument(arg_name, *args, **kwargs)
    arg_list.append(arg_name)


def arg_index(arg_list, arg):
    for i in range(len(arg_list)):
        if arg_list[i].startswith(arg):
            return i
    raise ValueError


def arg_to_snake(s):
    return reduce(lambda y, z: y + '_' + z,
                  filter(lambda x: x != '', s.split('-')))


def snake_to_arg(s):
    return '--' + reduce(lambda y, z: y + '-' + z,
                         filter(lambda x: x != '', s.lower().split('_')))


def strtobool(s):
    if s.lower() in ['true', 'yes', 'ja']:
        return True
    if s.lower() in ['false', 'no', 'nein']:
        return False
    raise ValueError('What the hell is this supposed to be: %s?' % s)


def update_test_settings(arguments, cleanup_list):
    for attr_name in cleanup_list:
        argument_attr_name = arg_to_snake(attr_name)
        snake_attr_name = argument_attr_name.swapcase()
        if hasattr(config, snake_attr_name) and hasattr(arguments, argument_attr_name):
            new_value = getattr(arguments, argument_attr_name)
            if new_value:
                old_value = getattr(config, snake_attr_name)
                if type(old_value) == bool:
                    new_value = strtobool(new_value)
                setattr(config, snake_attr_name, new_value)
                print("%s: %s -> %s" % (snake_attr_name, old_value, new_value))


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

    parser = argparse.ArgumentParser(description='Will execute behavioral'
                                                 '(default) or api tests and '
                                                 'can also override some of the'
                                                 ' test user data')

    cleanup_list = []
    for attr in dir(config):
        if not isinstance(attr, types.FunctionType):
            if isinstance(attr, basestring):
                if attr.startswith('__') or attr.islower():
                    continue

            arg = snake_to_arg(attr)
            # log.info("Adding variable %s(%s, %s) from config to list of
            # params" % (attr, arg, type(arg)))
            prepare_arg_parser(parser, cleanup_list, arg, default=None)

    prepare_arg_parser(parser, cleanup_list, '--gui', action='store_true')
    prepare_arg_parser(parser, cleanup_list, '--api', action='store_true')

    args = parser.parse_known_args()[0]

    if args.gui and args.api:
        raise Exception("You must either provide the gui or the api flag but "
                        "not both. If you provide no flag then the behave will"
                        " be invoked")

    update_test_settings(args, cleanup_list)

    # Make sure to remove any args before handing over to the behave or the
    # py.test main to prevent errors
    args_to_be_cleaned = sys.argv[1:]
    clean_args(args_to_be_cleaned, cleanup_list)

    if args.gui or not args.api:
        import behave.__main__
        sys.exit(behave.__main__.main(args_to_be_cleaned))
    else:
        import pytest
        sys.exit(pytest.main(args_to_be_cleaned))
