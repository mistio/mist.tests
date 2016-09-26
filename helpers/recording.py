import os
import subprocess

from shlex import split

from time import time
from time import sleep

import logging

log = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)


def start_recording(output='test.mp4', dimension='1024x768',
                    display_num='1'):
    if os.path.isfile(output):
        os.remove(output)
    command = 'ffmpeg -f x11grab -video_size %s ' \
              '-i 127.0.0.1:{0} -codec:v libx264 -r 12 ' \
              '%s'.format(display_num, dimension, output)
    return subprocess.Popen(split(command), stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            stdin=subprocess.PIPE, bufsize=0)


def stop_recording(recording_process):
    return_code = recording_process.poll()
    if not return_code:
        recording_process.communicate('q\n')
        log.info("Sent terminating character to recording process")
        timeout = time() + 20
        while time() < timeout:
            if recording_process.poll() is not None:
                log.info("Recording process has terminated")
                break
            log.info("Waiting for recording process to terminate")
            sleep(1)
        else:
            recording_process.kill()
            raise Exception("Could not correctly terminate subprocess for "
                            "selenium recording")
    else:
        raise Exception("Seems like subprocess for selenium recording "
                        "terminated before the end of the tests")
