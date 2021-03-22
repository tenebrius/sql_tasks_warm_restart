import math
import os
import signal
import sys
from logging.handlers import RotatingFileHandler
from time import sleep

from sqs_workers import SQSEnv, create_standard_queue

import logging

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
logger = logging.getLogger()
logger.setLevel("INFO")

# fileHandler = logging.FileHandler("tasks.log")
fileHandler = RotatingFileHandler("tasks.log", maxBytes=math.pow(10, 7), backupCount=5)
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

# consoleHandler = logging.StreamHandler()
# consoleHandler.setFormatter(logFormatter)
# rootLogger.addHandler(consoleHandler)


logger.info("starting")


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = handle_exception


def writePidFile():
    pid = str(os.getpid())
    f = open('.pid', 'w')
    f.write(pid)
    f.close()


writePidFile()

# This environment will use AWS requisites from ~/.aws/ directory
sqs = SQSEnv()

# Create a new queue.
# Note that you can use the AWS web interface for the same action as well, the
# web interface provides more options. You only need to do it once.
create_standard_queue(sqs, "emails")

# Get the queue object
queue = sqs.queue("emails")


class ScheduledShutdown(object):
    """
    Shutdown worker if it's idle for certain time (set in seconds)
    """


    def __init__(self):
        pass

    def update_state(self, batch_processing_result):
        pass

    def need_shutdown(self):
        logger.info("checking for shutdown file")
        file_exist =  os.path.exists(".need_shutdown")
        if file_exist:
            os.remove(".need_shutdown")
            os.remove(".pid")
            logger.info("Scheduled shutdown activated")
            if os.path.exists(".need_shutdown"):
                logger.info("could not delete shutdown file")

        return file_exist

    def __repr__(self):
        return f"ScheduledShutdown"


# Register a queue processor
@queue.processor("send_email")
def send_email(to, subject, body):
    x = 0
    while x < 30:
        sleep(2)
        x = x + 1
        logger.info(f"Sending email {subject} to {to} {x}")
