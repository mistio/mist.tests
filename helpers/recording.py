import os
import subprocess

#from shlex import split

from time import time
from time import sleep

from threading import Thread
from threading import Lock

import logging

log = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)


kill_recording_process = False
recording_process_lock = Lock()
recording_sub_process = None


def start_recording(output='test.mp4', dimension='1024x768',
                    display_num='1'):
    log.info("Starting recording of the session!!!")
    if os.path.isfile(output):
        os.remove(output)
    # command = 'ffmpeg -f x11grab -video_size {0} -i :0.0 ' \
    #           '-codec:v libx264 -r 12 {2}'.format(dimension, display_num, output)

    command = 'ffmpeg -video_size 1024x768 -framerate 25 -f x11grab -i 127.0.0.1:{1} test.mp4'.format(dimension,display_num,output)

    print command
    global recording_sub_process
    # recording_sub_process = subprocess.Popen(split(command),
    #                                          stdout=subprocess.PIPE,
    #                                          stderr=subprocess.STDOUT,
    #                                          stdin=subprocess.PIPE,
    #                                          shell=True,
    #                                          bufsize=0)
    #
    recording_sub_process = subprocess.Popen(command.split())

    # thr = Thread(target=discard_output,
    #              args=[recording_sub_process])
    # thr.daemon = True
    # thr.start()
    # global kill_recording_process
    #
    # while not kill_recording_process:
    #     sleep(1)
    #
    # thr.kill()


def discard_output(sub_process):
    log.info("Started recording subprocess and handling thread")
    global kill_recording_process
    global recording_process_lock
    recording_process_lock.acquire()
    while not kill_recording_process:
        sub_process.stdout.readline()
    log.info("Stopped discarding output and proceeding to kill process")
    timeout = time() + 20
    while time() < timeout:
        if sub_process.poll() is not None:
            log.info("Recording process has terminated")
            recording_process_lock.release()
            break
        log.info("Waiting for recording process to terminate")
        sleep(1)
    else:
        sub_process.kill()
        recording_process_lock.release()
        raise Exception("Could not correctly terminate subprocess for "
                        "selenium recording")




def stop_recording():
    log.info("Stopping recording of the session")
    global kill_recording_process
    global recording_sub_process
    kill_recording_process = True
    log.info("Sent terminating character to recording process")
    recording_sub_process.stdin.write('q\n')
    recording_process_lock.acquire()
