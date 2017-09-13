import os
import subprocess

from shlex import split

from time import time
from time import sleep

from threading import Thread
from threading import Lock

from multiprocessing import Process, Queue

import logging

log = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)


kill_recording_process = False
recording_process_lock = Lock()
recording_sub_process = None


#    global recording_sub_process
#    recording_sub_process = subprocess.Popen(split(command),
#                                             stdout=subprocess.PIPE,
#                                             stderr=subprocess.STDOUT,
#                                             stdin=subprocess.PIPE,
#                                             bufsize=0)

#    thr = Thread(target=discard_output,
#                 args=[recording_sub_process])
#    thr.daemon = True
#    thr.start()


def take_screenshot(context):
    context.browser.get_screenshot_as_file('testit.png')

def start_recording(context):
    log.info("Starting recording of the session")

    #queue = Queue()
    #p = Process(target=start_taking_screenshots, args=(queue, context))
    #p.start()

    command = start_taking_screenshots(context)
    global recording_sub_process
    recording_sub_process = subprocess.Popen(split(command),
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.STDOUT,
                                             stdin=subprocess.PIPE,
                                             bufsize=0)

    thr = Thread(target=discard_output,
                 args=[recording_sub_process])
    thr.daemon = True
    thr.start()

def start_taking_screenshots(context):

    schedule.every(10).seconds.do(take_screenshot, context)


    #while 1:
    #    schedule.run_pending()
    #    sleep(1)

    #cron = CronTab()
    #job = cron.new(command=take_screenshot(context))
    #cron.write()
    #job.hour.every(4)

    #cron.write()


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
    try:
        recording_sub_process.communicate(input='q\n')
        log.info("Sent terminating character to recording process")
    except:
        pass
    recording_process_lock.acquire()
