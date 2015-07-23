#!coding: utf-8
__author__ = 'zkchen'
import time
from django.utils import timezone
from tmkit.runtask import task_manager, as_task
from tmkit.runtask.models import Task


# TODO 还没想好怎么写下去
# @as_task(name="check_task_thread")
def check_task_thread(*args, **kwargs):
    delay = 3
    while True:
        time.sleep(delay)
        for func, thread_list in task_manager.thread_map.items():
            for th in thread_list:
                if th.ident:
                    try:
                        task = Task.objects.get(thread_ident=th.ident)
                    except Task.DoesNotExist:
                        task = Task(task_name=th.getName(), last_response=timezone.now(),
                                    group=func.task_name, thread_ident=th.ident)
                        task.save()


