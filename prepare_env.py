import os
import sys
import argparse

import config


def argument_cleanup_list(parser, arg_list, arg_name, *args, **kwargs):
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

    parser = argparse.ArgumentParser(description='Will execute behavioral '
                                                 'tests and can also override '
                                                 'some of the test user data')
    cleanup_list = []
    argument_cleanup_list(parser, cleanup_list, '--email', default=None)
    argument_cleanup_list(parser, cleanup_list, '--name', default=None)
    argument_cleanup_list(parser, cleanup_list, '--password1', default=None)
    argument_cleanup_list(parser, cleanup_list, '--password2', default=None)
    argument_cleanup_list(parser, cleanup_list, '--mist-url', default=None)
    argument_cleanup_list(parser, cleanup_list, '--js-console-log', default=None)
    argument_cleanup_list(parser, cleanup_list, '--webdriver-log', default=None)
    argument_cleanup_list(parser, cleanup_list, '--test-output-log', default=None)
    argument_cleanup_list(parser, cleanup_list, '--screenshot-path', default=None)
    argument_cleanup_list(parser, cleanup_list, '--browser-flavor', default=None)
    argument_cleanup_list(parser, cleanup_list, '--local', default=None)
    argument_cleanup_list(parser, cleanup_list, '--mist-dir', default=None)
    argument_cleanup_list(parser, cleanup_list, '--xvfb-display', default=None)
    argument_cleanup_list(parser, cleanup_list, '--webdriver-path', default=None)

    args = parser.parse_known_args()[0]
    # print "Args submitted: " + str(args)
    update_test_settings(args, cleanup_list)

    if args.xvfb_display:
        print("Exporting DISPLAY variable(%s)" % args.xvfb_display)
        os.environ['DISPLAY'] = ':%s.0' % args.xvfb_display

    # Make sure to remove my args before handing over to the behave main
    args_to_be_cleaned = sys.argv[1:]
    clean_args(args_to_be_cleaned, cleanup_list)
    # print "Args to be passed on to behave:" + str(args_to_be_cleaned)

    import behave.__main__
    sys.exit(behave.__main__.main(args_to_be_cleaned))

