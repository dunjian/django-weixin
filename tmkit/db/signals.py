#!coding: utf-8
__author__ = 'zkchen'
from django.dispatch import Signal, receiver


sig_virtual_deletion = Signal(providing_args=["obj"])
sig_virtual_rollback = Signal(providing_args=["obj"])





