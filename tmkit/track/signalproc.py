#!coding: utf-8
__author__ = 'zkchen'
from datetime import datetime
import time

from django.dispatch import receiver

from signals import sig_500, sig_404
from .models import Entry


def record_err(err_code, **kwargs):
    request = kwargs.get("request")
    response = kwargs.get("response")
    timestamp = getattr(request, "timestamp", time.time())
    cost_time = getattr(response, "cost_time", 0)
    entry = Entry()
    try:
        entry.body = request.body
    except:
        entry.body = ""
    entry.content = "".join([c for c in response])
    entry.cost_time = cost_time
    entry.method = request.method
    entry.path = request.get_full_path()
    entry.request_header = str(request.META)
    entry.request_time = datetime.fromtimestamp(timestamp)
    entry.response_header = str(response._headers)
    entry.size = len(entry.body)
    entry.status_code = err_code or 0
    entry.save()


@receiver(sig_500)
def process_sig_500(sender, **kwargs):
    record_err(500, **kwargs)


@receiver(sig_404)
def process_sig_404(sender, **kwargs):
    record_err(404, **kwargs)
