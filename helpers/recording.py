import os
import subprocess
import signal

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

def start_recording(context,output='test.mp4', dimension='1024x768',
                    display_num='1'):
    log.info("Starting recording of the session!!!")
    if os.path.isfile(output):
        os.remove(output)
    # command = 'ffmpeg -f x11grab -video_size {0} -i :0.0 ' \
    #           '-codec:v libx264 -r 12 {2}'.format(dimension, display_num, output)

    num = context.mist_config['ERROR_NUM_MP4'] = context.mist_config['ERROR_NUM_MP4'] + 1
    command = 'ffmpeg -video_size 1024x768 -framerate 25 -f x11grab ' \
              '-i 127.0.0.1:{1} '

    path = context.mist_config['VIDEO_PATH'] + 'test{0}.mp4'.format(str(num))

    command = (command + path).format(dimension,display_num,output)

    global recording_sub_process
    recording_sub_process = subprocess.Popen(command.split(),stdin=subprocess.PIPE,
                                             stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    # import ipdb
    # ipdb.set_trace()
    thr = Thread(target=discard_output,
                 args=[recording_sub_process])
    thr.daemon = True
    thr.start()

def discard_output(sub_process):
    log.info("Started recording subprocess and handling thread")
    global kill_recording_process
    global recording_process_lock
    recording_process_lock.acquire()
    while not kill_recording_process:
        sub_process.stdout.readline()
    log.info("Stopped discarding output and proceeding to kill process")
    # import ipdb
    # ipdb.set_trace()
    timeout = time() + 20
    while time() < timeout:
        if sub_process.poll() is not None:
            log.info("Recording process has terminated")
            recording_process_lock.release()
            break
        #log.info("Waiting for recording process to terminate")
        sleep(1)
    else:
        sub_process.kill()
        recording_process_lock.release()
        raise Exception("Could not correctly terminate subprocess for "
                        "selenium recording")


def stop_recording():
    global kill_recording_process
    global recording_sub_process
    kill_recording_process = True
    recording_sub_process.stdin.write('q\n')
    log.info("Sent terminating character to recording process")
    # import ipdb
    # ipdb.set_trace()
    #recording_process_lock.acquire()

# def kill_mayday_recording():
#     os.killpg(os.getpgid(recording_sub_process.pid),signal.SIGTERM)