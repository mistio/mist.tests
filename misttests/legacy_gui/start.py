import re
import os
import sys
import json
import uuid
import shutil
import argparse
import subprocess

from time import time
from time import sleep

from shlex import split

from threading import Lock
from threading import Thread


def get_process_dict():
    return {
        'uuid': None,
        'command': '',
        'fps': [],
        'runs': 0,
        'reruns': 0,
        'close_streams': True,
        'identifier': None,
        'process': None,
        'thread_handler_start_time': 0,
        'started': False,
        'return_value': 0,
        'features': {
            'passed': 0,
            'failed': 0,
            'skipped': 0
        },
        'scenarios': {
            'passed': 0,
            'failed': 0,
            'skipped': 0
        },
        'steps': {
            'passed': 0,
            'failed': 0,
            'skipped': 0,
            'undefined': 0
        }
    }


def handle_proc_output(thread_sync_dict,
                       process_dict,
                       tail_output=True):
    process_dict['thread_handler_start_time'] = time()
    command = process_dict['command']
    identifier = process_dict['identifier']
    thread_sync_dict['lock'].acquire()
    thread_sync_dict['last_thread_print'] = identifier
    print "\nExecuting :\n%s" % command
    thread_sync_dict['lock'].release()

    process_dict['process'] = proc = subprocess.Popen(split(command),
                                                      stdout=subprocess.PIPE,
                                                      stderr=subprocess.STDOUT,
                                                      bufsize=0)

    while True:
        output = proc.stdout.readline()
        if output:
            if re.search(".*Finished with before_all hook.*", output):
                process_dict['started'] = True
            match = re.search("(?P<passed>\d+) features? passed, "
                              "(?P<failed>\d+) failed, "
                              "(?P<skipped>\d+) skipped", output)
            if match:
                process_dict['features']['passed'] += int(match.group('passed'))
                process_dict['features']['failed'] += int(match.group('failed'))
                process_dict['features']['skipped'] += int(
                    match.group('skipped'))
            match = re.search("(?P<passed>\d+) scenarios? passed, "
                              "(?P<failed>\d+) failed, "
                              "(?P<skipped>\d+) skipped", output)
            if match:
                process_dict['scenarios']['passed'] += int(
                    match.group('passed'))
                process_dict['scenarios']['failed'] += int(
                    match.group('failed'))
                process_dict['scenarios']['skipped'] += int(
                    match.group('skipped'))
            match = re.search("(?P<passed>\d+) steps? passed, "
                              "(?P<failed>\d+) failed, "
                              "(?P<skipped>\d+) skipped, "
                              "(?P<undefined>\d+) undefined", output)
            if match:
                process_dict['steps']['passed'] += int(match.group('passed'))
                process_dict['steps']['failed'] += int(match.group('failed'))
                process_dict['steps']['skipped'] += int(match.group('skipped'))
                process_dict['steps']['undefined'] += int(
                    match.group('undefined'))
            if tail_output:
                thread_sync_dict['lock'].acquire()
                if thread_sync_dict['last_thread_print'] != identifier:
                    thread_sync_dict['last_thread_print'] = identifier
                    sys.stdout.write(
                        '\n\nOutput from %s container:\n' % identifier)
                    # Strip the Cursor Up characters to fix file printing
                    sys.stdout.write(re.sub("\\x1b\[\d*A", "", output))
                else:
                    # sys.stdout.write(re.sub("\\x1b\[\d*A", "\x1b[1A", output))
                    sys.stdout.write(output)
                sys.stdout.flush()
                thread_sync_dict['lock'].release()
            for fp in process_dict['fps']:
                fp.write(output)
                fp.flush()
        process_dict['return_value'] = proc.poll()
        if process_dict['return_value'] is not None:
            process_dict['return_value'] = proc.poll()
            thread_sync_dict['lock'].acquire()
            print("Return code of container %s is %s" % (
            identifier, process_dict['return_value']))
            thread_sync_dict['lock'].release()
            break
    proc.stdout.close()

    thread_sync_dict['lock'].acquire()
    for i in range(len(thread_sync_dict['process_list'])):
        if thread_sync_dict['process_list'][i]['uuid'] == process_dict['uuid']:
            thread_sync_dict['process_list'].pop(i)
            break
    thread_sync_dict['finished_tests'].append(process_dict)
    thread_sync_dict['active_threads'] -= 1
    thread_sync_dict['lock'].release()


def prepare_docker_command(docker_image_name, mist_dir,
                           network_type='bridge', tags=None, email=None,
                           user_password1=None, user_password2=None,
                           name=None, mist_url=None, js_console_log=None,
                           webdriver_log=None, test_output_log=None,
                           screenshot_path=None, browser_flavor=None,
                           test_type='pr', xvfb=1, local=False):
    command = 'docker run -v=%s:/mnt/mist.core ' \
              '--net="%s" ' % (mist_dir, network_type)

    if tags:
        if type(tags) == list:
            command += '-e TAGS=\"--tags=%s\" ' % ','.join(tags)
        else:
            command += '-e TAGS=\"--tags=%s\" ' % tags

    sed_dir = mist_dir.replace('/', '\/').replace('.', '\.').replace(' ', '\ ')
    command += "-e SED_REGEX=\"%s\" " % sed_dir
    prepare_environment = ''

    if local is not None:
        prepare_environment += '--local %s ' % local

    if email:
        prepare_environment += '--email %s ' % email

    if name:
        prepare_environment += '--name %s ' % name

    if user_password1:
        prepare_environment += '--user-password1 %s ' % user_password1

    if user_password2:
        prepare_environment += '--user-password2 %s ' % user_password2

    if mist_url:
        prepare_environment += '--mist-url %s ' % mist_url

    if js_console_log:
        prepare_environment += '--js-console-log %s ' % os.path.join(
            '/mnt/mist.core', js_console_log)

    if webdriver_log:
        prepare_environment += '--webdriver-log %s ' % os.path.join(
            '/mnt/mist.core', webdriver_log)

    if screenshot_path:
        prepare_environment += '--screenshot-path %s ' % os.path.join(
            '/mnt/mist.core', screenshot_path)

    if browser_flavor:
        prepare_environment += '--browser-flavor %s ' % browser_flavor

    if xvfb:
        prepare_environment += '--xvfb-display %s ' % xvfb
        command += '-e XVFB_NUM=%s ' % xvfb

    if test_output_log:
        command += '-e OUTFILE=\"-o %s\" ' % os.path.join('/mnt/mist.core',
                                                          test_output_log)

    command += '-e TEST_TYPE=\"%s\" ' % test_type

    if prepare_environment:
        command += '-e PREP_ENV="%s" ' % prepare_environment

    command += '-t %s' % docker_image_name

    return command


def check_user_file(path_to_json, min_num_of_users):
    fp = open(path_to_json, 'r')
    user_json = json.load(fp)
    users = 0
    for user in user_json:
        if not user.get('password'):
            fp.close()
            raise ValueError('User %s has no password' % user)
        users += 1
    if users < min_num_of_users:
        raise ValueError('Too few users to run %s tests' % min_num_of_users)
    return user_json


def poll_until_timeout(command, proc, timeout=10):
    return_code = proc.poll()
    timeout = time() + 10
    while return_code is None and time() < timeout:
        sleep(1)
        return_code = proc.poll()
    if return_code is None:
        print("Waited for too long(%s) for command %s to finish\n. "
              "Exiting\n" % (command, timeout))
        sys.exit(1)
    return return_code


def fix_dir(d):
    return d.replace('.', '\.').replace(' ', '\ ')


def subprocess_pipeline(commands,
                        print_pipeline_steps=False,
                        ignore_non_zero_return_code=False):
    output = None
    prev_input = None
    prev_exit_code = None

    for command in commands:
        kwargs = {
            'stdout': subprocess.PIPE,
            'stderr': subprocess.STDOUT
        }
        if prev_exit_code is not None:
            kwargs.update({'stdin': subprocess.PIPE})
        proc = subprocess.Popen(split(command), **kwargs)
        if prev_exit_code is not None:
            output, _ = proc.communicate(prev_input)
            return_code = proc.poll()
        else:
            output = proc.stdout.read()
            return_code = poll_until_timeout(command, proc)
        if return_code != 0:
            print('return code of %s was %s and ' % (command,
                                                     return_code))
        if print_pipeline_steps:
            print("For command %s input is:\n%s\noutput is:\n %s" % (command,
                                                                     prev_input,
                                                                     output))
        if not ignore_non_zero_return_code and return_code != 0:
            sys.exit(return_code)
        elif not output:
            break
        prev_exit_code = return_code
        prev_input = output

    return output


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Start multiple containerized"
                                                 " behave tests")

    parser.add_argument('--mist-url', default=None, required=False,
                        help="The url to the mist instance to be tested")
    parser.add_argument('--log-dir', default='var/log',
                        help="Path to the directory where the logs will be "
                             "stored")
    parser.add_argument('--tags', required=False, default=[],
                        help="Scenario and feature tags that will be executed. "
                             "If it is empty then all the tests in the "
                             "directory will be executed")
    parser.add_argument('--docker-img', default='mist_behave', required=False,
                        help="Tag of the docker image to be executed")
    parser.add_argument('--mount-dir', default=os.getcwd(), required=False,
                        help="The directory with the mist.core code that will "
                             "be mounted to the docker container. If not "
                             "provided it defaults to the current working "
                             "directory")
    parser.add_argument('--force-bld-img',
                        action='store_true', default=False, required=False,
                        help="If set, the program will try to build the docker "
                             "image even if it already exists")
    parser.add_argument('--dkr-img-path', dest='docker_image_path',
                        default='src/mist/core/tests/gui/',
                        help="Path to the Dockerfile")
    parser.add_argument('--user-json-path', required=False,
                        help="Path to a json file with users that will be used "
                             "to extract emails and credentials")
    parser.add_argument('--users', required=False, nargs='+',
                        help="User that will be used for running tags in "
                             "parallel. Only one user can be supplied and "
                             "should be given in the form email:password1:"
                             "password2:name. Any of the fields"
                             "can be missing except the email")
    parser.add_argument('--tail-output', required=False, default=False,
                        action='store_true')
    parser.add_argument('--executors', required=False, default=-1,
                        help="Max number of containers that will be running"
                             " in parallel")
    parser.add_argument('--clean-dir', required=False, default=[],
                        help="Clean some directory because containers can't "
                             "do that", nargs='*')
    parser.add_argument('--test-type', required=False, default='',
                        help="Type of tests to be run for example pr for pull "
                             "request tests, stress for stress tests")
    parser.add_argument('--reruns', required=False, default=0, type=int,
                        help="number of times to rerun failed tests")
    parser.add_argument('--timeout', required=False, default=-1, type=int,
                        help="Seconds after which if tests haven't started a"
                             "container is killed")

    params = parser.parse_known_args(sys.argv[1:])[0]

    for folder in params.clean_dir:
        shutil.rmtree(folder, ignore_errors=True)

    dkr_images = subprocess_pipeline(['docker images',
                                      'grep "%s"' % params.docker_img,
                                      "awk '{print $1}'"],
                                     print_pipeline_steps=False,
                                     ignore_non_zero_return_code=True).strip()
    if not dkr_images.strip() or params.force_bld_img:
        dkr_com = "docker build -t %s %s" % (params.docker_img,
                                             params.docker_image_path)
        print "Building Docker image with command:\n %s" % dkr_com

        build_process = subprocess.Popen(split(dkr_com),
                                         stdout=sys.stdout,
                                         stderr=subprocess.STDOUT)
        poll_until_timeout(dkr_com, build_process, 200)

        dkr_images = subprocess_pipeline(['docker images',
                                          'grep "%s"' % params.docker_img,
                                          "awk '{print $1}'"]).strip()

        if not dkr_images.strip():
            print "Failed to build Docker image. Exiting"
            sys.exit(-1)

    print "\nDocker image %s is ready!" % params.docker_img

    # This dictionary will pe passed around to the threads in order to help them
    # synchronize and provide them with important information about their
    # function
    thread_sync_dict = {
        'finished_tests': list(),
        'process_list': list(),
        'active_threads': 0,
        'last_thread_print': '',
        'lock': Lock()
    }

    # This dictionary will be used solely by the thread that oversees all the
    # other processes. It is used to track the progress of the threads,
    # how many threads there are and if any processes need to be rerun if they
    # fail.
    work_overview_dict = {
        'work_queue': list(),
        'finalized_tests': list(),
        'threads': list(),
    }

    # Get tags of behave tests to run
    tags = params.tags.split(',') if params.tags else []

    # Get the user/s that will run the tests
    users = dict()
    if params.users:
        for user in params.users:
            email, password1, password2, first_name, last_name = user.split(':')
            if users.get(email, None) is not None:
                raise Exception('User with email %s was provided twice' % email)
            else:
                users[email]['password1'] = password1
                users[email]['password2'] = password2
                users[email]['first_name'] = first_name
                users[email]['last_name'] = last_name
    elif params.user_json_path:
        users = check_user_file(params.user_json_path, params.test_users)

    executors = int(params.executors) if params.executors else -1
    if executors == 0 or executors < -1:
        raise Exception("Can not proceed. Wrong number of executors(%s) "
                        "provided" % executors)
    reruns = int(params.reruns) if params.reruns else 0
    timeout = int(params.timeout) if params.timeout else -1

    if len(users.keys()) <= 1:
        kwargs = {
            'network_type': 'host',
            'mist_url': params.mist_url,
            'test_type': params.test_type
        }
        if len(users.keys()) == 1:
            # if a user has been provided then use his email and creds
            email = users[users.keys()[0]]
            print "User %s will be used" % email
            kwargs.update({
                'email': email,
                'user_password1': users[email]['password1'],
                'user_password2': users[email]['password2'],
                'name': users[email]['name'],
            })
        else:
            print "The user from the configuration file will be used"

        if len(tags) == 0:
            # The default user in the test config will be used for all the
            # behavioral tests
            print "No tags where provided"
            if len(users.keys()) == 1:
                identifier = email
            else:
                identifier = "docker"
            kwargs.update({
                'js_console_log': os.path.join(params.log_dir,
                                               'js.console.%s.log' % identifier),
                'webdriver_log': os.path.join(params.log_dir,
                                              'webdriver.%s.log' % identifier),
                'screenshot_path': os.path.join(params.log_dir,
                                                'error.%s' % identifier),
                'test_type': params.test_type
            })
            process_dict = get_process_dict()
            process_dict['command'] = prepare_docker_command(params.docker_img,
                                                             params.mount_dir,
                                                             **kwargs)
            process_dict['fps'].append(
                open(os.path.join(params.log_dir, 'docker_test.log'), 'a'))
            process_dict['identifier'] = identifier
            process_dict['reruns'] = reruns
            work_overview_dict['work_queue'].append(process_dict)
        else:
            # One user has been given and he will be used to execute all the
            # tags provided
            print "Tags provided are %s" % tags
            xvfb = 1
            for tag in tags:
                identifier = tag
                kwargs.update({
                    'tags': tag,
                    'js_console_log': os.path.join(params.log_dir,
                                                   'js.console.%s.log' % identifier),
                    'webdriver_log': os.path.join(params.log_dir,
                                                  'webdriver.%s.log' % identifier),
                    'screenshot_path': os.path.join(params.log_dir,
                                                    'error.%s' % identifier),
                    'test_type': params.test_type,
                    'xvfb': xvfb
                })
                process_dict = get_process_dict()
                process_dict['command'] = prepare_docker_command(
                    params.docker_img,
                    params.mount_dir,
                    **kwargs)
                process_dict['fps'].append(
                    open(os.path.join(params.log_dir, 'docker_test.log'), 'a'))
                process_dict['identifier'] = identifier
                process_dict['reruns'] = reruns
                work_overview_dict['work_queue'].append(process_dict)
                xvfb += 1

    print "Starting threads"
    if executors == -1:
        executors = len(work_overview_dict['work_queue'])
    while True:
        thread_sync_dict['lock'].acquire()

        # If a timeout has been given by the user then check if a container
        # has exceeded the timeout
        if timeout > 0:
            for process_dict in thread_sync_dict['process_list']:
                started = process_dict['started']
                boot_time = time() - process_dict['thread_handler_start_time']
                if not started and boot_time >= timeout:
                    if not started:
                        print "Process for command %s has not booted " \
                              "yet(%s, %s)" % (started, boot_time)
                    thread_sync_dict['last_thread_print'] = "master"
                    print "Killing process started with command " \
                          "%s" % process_dict['command']
                    if process_dict.get('process', None) is not None:
                        process_dict['process'].kill()

        # if there is a test that has finished check if it crashed or
        # if it finished normally
        for i in range(len(thread_sync_dict['finished_tests'])):
            finished_test = thread_sync_dict['finished_tests'].pop()
            # check if a finished test must be restarted or should
            # be added to the list of finalized tests
            if finished_test['reruns'] > 0 and \
                    finished_test['return_value'] != 0 and \
                    finished_test['features']['passed'] == 0 and \
                    finished_test['features']['failed'] == 0 and \
                    finished_test['features']['skipped'] == 0:
                process_dict = get_process_dict()
                process_dict['reruns'] = finished_test['reruns'] - 1
                process_dict['command'] = finished_test['command']
                process_dict['close_streams'] = finished_test['close_streams']
                process_dict['identifier'] = finished_test['identifier']
                process_dict['fps'] = finished_test['fps']
                thread_sync_dict['last_thread_print'] = "master"
                print "Readding container for command\n%s\n back " \
                      "to work queue. Reruns left:" \
                      " %s" % (process_dict['command'],
                               process_dict['reruns'])
                work_overview_dict['work_queue'].append(
                    process_dict)
            else:
                if finished_test['close_streams']:
                    for fp in finished_test['fps']:
                        fp.close()
                work_overview_dict[
                    'finalized_tests'].append(finished_test)

        # if there are available executors and work to be done then start
        # more work
        while len(work_overview_dict['work_queue']) > 0 and \
                thread_sync_dict['active_threads'] < executors:
            process_dict = work_overview_dict['work_queue'].pop(0)
            process_dict['runs'] += 1
            process_dict['uuid'] = uuid.uuid4()
            thread_sync_dict['last_thread_print'] = "master"
            print "Starting a new thread for identifier %s and " \
                  "command:\n%s" % (process_dict['identifier'],
                                    process_dict['command'])
            thr = Thread(target=handle_proc_output,
                         args=[thread_sync_dict, process_dict])
            thr.daemon = True
            thr.start()
            thread_sync_dict['active_threads'] += 1
            thread_sync_dict['process_list'].append(process_dict)

        if thread_sync_dict['active_threads'] == 0 and \
                len(work_overview_dict['work_queue']) == 0:
            thread_sync_dict['lock'].release()
            print "Finished work"
            break

        thread_sync_dict['lock'].release()
        sleep(2)

    container_results = work_overview_dict['finalized_tests']

    final_results = get_process_dict()
    categories = ['passed', 'skipped', 'failed']
    for thingie1 in ['features', 'scenarios', 'steps']:
        if thingie1 == 'steps':
            categories.append('undefined')
        for thingie2 in categories:
            final_results[thingie1][thingie2] = reduce(
                lambda x, y: x + y.get(thingie1, {}).get(thingie2, 0),
                container_results, 0)

    final_results['return_value'] = reduce(
        lambda x, y: x + y.get('return_value', 0),
        container_results, 0)

    failed_containers = len(filter(lambda x: x['return_value'] != 0 and
                                             x['features']['passed'] == 0 and
                                             x['features']['failed'] == 0 and
                                             x['features']['skipped'] == 0,
                                   container_results))

    print """Final results are:
    {0} features passed, {1} failed, {2} skipped
    {3} scenarios passed, {4} failed, {5} skipped
    {6} steps passed, {7} failed, {8} skipped, {9} undefined
    {10} containers failed
    """.format(final_results['features']['passed'],
               final_results['features']['failed'],
               final_results['features']['skipped'],
               final_results['scenarios']['passed'],
               final_results['scenarios']['failed'],
               final_results['scenarios']['skipped'],
               final_results['steps']['passed'],
               final_results['steps']['failed'],
               final_results['steps']['skipped'],
               final_results['steps']['undefined'],
               failed_containers)

    print "Exit codes of the containers are: %s" % str(
        map(lambda x: x['return_value'], container_results))

    if final_results['return_value'] != 0:
        sys.exit(final_results['return_value'])

    sys.exit(final_results['features']['failed'] +
             final_results['scenarios']['failed'] +
             final_results['steps']['failed'] +
             final_results['steps']['undefined'])
