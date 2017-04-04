import argparse
import types
import sys

from misttests import config

from prepare_env import snake_to_arg, prepare_arg_parser

API_TESTS = ['clouds', 'machines', 'keys', 'scripts', 'images', 'api_token',
             'tunnels', 'schedules']

ui_tests_features = {
    'clouds': ['clouds-actions', 'clouds-add-a', 'clouds-add-b'],
    'images': ['images-networks'],
    'keys': ['keys'],
    'machines': ['orchestration'],
    'rbac': ['rbac-rules', 'rbac-teams'],
    'schedules': ['schedulers', 'schedulers_v2'],
    'scripts': ['scripts'],
    'users': ['user-actions']
}



def get_pytest_args(args_given):
    pytest_args = []
    pytest_args.append('-s')
    for arg in args_given:
        api_test_path = 'src/mist.io/tests/misttests/api/core/' + arg.strip('-') + '.py'
        pytest_args.append(api_test_path)
    return pytest_args


def get_behave_args(args_given):
    behave_args = []
    behave_args.append('-k')
    behave_args.append('--stop')
    tags_arg = '--tags='
    for arg in args_given:
        tag_values = ui_tests_features.get(arg.strip('-'))
        for tag in tag_values:
            tags_arg += tag
            tags_arg += ','
    behave_args.append(tags_arg)
    behave_args.append('src/mist.io/tests/misttests/gui/core/pr/features')
    return behave_args


def validate_args(args_to_be_cleaned, tests_type):
        for arg in args_to_be_cleaned:
            arg = arg.strip('-')
            if 'api' in tests_type and arg not in API_TESTS:
                raise Exception("Api tests can run on the following resources: clouds, machines, keys, "
                                "scripts, images, api_token, tunnels, schedules")
            if 'gui' in tests_type and arg not in ui_tests_features.keys():
                raise Exception("UI tests can run on the following resources: clouds, machines, keys, "
                                "scripts, images, users, rbac, schedules")


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

    if len(sys.argv) < 2:
        raise Exception("You must either provide the gui or the api flag.")
    elif args.gui and args.api:
        raise Exception("You must either provide the gui or the api flag but "
                        "not both.")
    elif args.gui:
        if len(args_to_be_cleaned) > 0:
            validate_args(args_to_be_cleaned, 'gui')
            behave_args = get_behave_args(args_to_be_cleaned)
            import behave.__main__
            sys.exit(behave.__main__.main(behave_args))
        else:
            raise Exception("For UI tests you have to specify one of the following resources: clouds, machines, keys, "
                                "scripts, images, users, rbac, schedules")
    elif args.api:
        if len(args_to_be_cleaned) > 0:
            validate_args(args_to_be_cleaned, 'api')
            pytest_args = get_pytest_args(args_to_be_cleaned)
        else:
            pytest_args = get_pytest_args(API_TESTS)
            import ipdb;ipdb.set_trace()
        import pytest
        sys.exit(pytest.main(pytest_args))
    else:
        raise Exception("You must either provide the gui or the api flag.")
