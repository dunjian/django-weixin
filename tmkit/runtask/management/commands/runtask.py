#!coding: utf-8
__author__ = 'zkchen'
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.module_loading import autodiscover_modules
from tmkit.runtask import task_manager, TaskThreadWrapper


logger = settings.LOGGER


class Command(BaseCommand):
    def handle(self, *args, **options):
        super(Command, self).handle(*args, **options)

    def execute(self, *args, **options):
        autodiscover_modules("task")
        task_manager.run_task()

