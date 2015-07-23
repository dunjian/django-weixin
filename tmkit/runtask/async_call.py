#!coding:utf-8
__author__ = 'akun'

import logging
import Queue
import threading


_task_queue = Queue.Queue()


def async_call(function, callback, *args, **kwargs):
    _task_queue.put({
        'function': function,
        'callback': callback,
        'args': args,
        'kwargs': kwargs
    })


def _task_queue_consumer():
    """
    异步任务队列消费者
    """
    while True:
        try:
            task = _task_queue.get()
            function = task.get('function')
            callback = task.get('callback')
            args = task.get('args')
            kwargs = task.get('kwargs')
            print("id:%s" % id(_task_queue))
            try:
                if callback:
                    callback(function(*args, **kwargs))
            except Exception as ex:
                if callback:
                    callback(ex)
            finally:
                _task_queue.task_done()
        except Exception as ex:
            logging.warning(ex)


def handle_result(result):
    print(type(result), result)


t = threading.Thread(target=_task_queue_consumer)
t.daemon = True
t.start()

