#!coding: utf-8
__author__ = 'zkchen'
import threading


ERROR = "error"
DEBUG = "debug"
INFO = "info"
WARNING = "warning"


class TaskManager(object):
    def __init__(self):
        self._task_list = []
        self._thread_map = {}

    def register(self, task, *args, **kwargs):
        if getattr(task, "task_name", None) is None:
            task.task_name = getattr(task, "func_name", task.__name__)
        self._task_list.append((task, args, kwargs))

    def run_task(self):
        """
        启动任务
        """
        thread_list = []
        for task in self.task_list:
            thread_list.append(self.as_thread(task))

        print(self._task_list)
        print(self._thread_map)

        [t.start() for t in thread_list]
        [t.join() for t in thread_list]

    @property
    def thread_map(self):
        return self._thread_map

    @property
    def task_list(self):
        return self._task_list

    def as_thread(self, task):
        for t in self._task_list:
            if t == task:
                func, args, kwargs = task
                th = TaskThreadWrapper(func, *args, **kwargs)
                th.setName("%s.%s" % (func.task_name, th.getName()))
                if func not in self._thread_map:
                    self._thread_map[func] = [th]
                else:
                    self._thread_map[func].append(th)
                return th
        raise RuntimeError(u"task %s not should be registered before using" % str(task))


class TaskThreadWrapper(threading.Thread):
    def __init__(self, func, *args, **kwargs):
        self.func, self.args, self.kwargs, = func, args, kwargs
        if not callable(self.func):
            raise RuntimeError(u"task %s must be callable" % str(self.func))
        super(TaskThreadWrapper, self).__init__()

    def run(self):
        self.func(*self.args, **self.kwargs)


def as_task(name=None, *args, **kwargs):
    def wrapper(func):
        if name:
            func.task_name = name
        task_manager.register(func, *args, **kwargs)
        return func
    return wrapper

task_manager = TaskManager()

