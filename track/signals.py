#!coding:utf-8
__author__ = 'akun'
from django.dispatch import Signal


sig_tracking_request = Signal(providing_args=["request"])
sig_tracking_before_tracking = Signal(providing_args=["request", "response"])
sig_tracking_after_tracking = Signal(providing_args=["request", "response"])
sig_404 = Signal(providing_args=["request", "response"])
sig_500 = Signal(providing_args=["request", "response"])
