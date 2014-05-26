from abc import ABCMeta, abstractmethod
import multiprocessing
from time import sleep
import uuid
import threading


class Scheduler:
    __metaclass__ = ABCMeta

    def __init__(self, seconds, code):
        self.seconds = seconds
        self.code = code

    def _decorate_task(self):
        def result():
            while (True):
                sleep(self.seconds)
                self.code()

        return result

    @abstractmethod
    def run(self):
        pass


class ThreadSimpleScheduler(Scheduler):
    def run(self):
        thread = threading.Thread(name='SCHEDULER-' + str(uuid.uuid4()), target=self._decorate_task())
        thread.daemon = True
        thread.start()
        return thread


class ProcessSimpleScheduler(Scheduler):
    def run(self):
        process = multiprocessing.Process(name='SCHEDULER-' + str(uuid.uuid4()), target=self._decorate_task())
        process.daemon = True
        process.start()
        return process





