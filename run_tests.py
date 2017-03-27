import argparse

from misttests import config

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

    if args.gui and args.api:
        raise Exception("You must either provide the gui or the api flag but "
                        "not both. If you provide no flag then the behave will"
                        " be invoked")
