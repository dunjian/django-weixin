#!coding: utf-8
__author__ = 'zkchen'
from datetime import datetime

from django.dispatch import receiver

from signals import sig_500, sig_404
from .models import Entry


@receiver(sig_500)
def process_sig_500(sender, **kwargs):
    request = kwargs.get("request")
    response = kwargs.get("response")
    timestamp = getattr(request, "timestamp")
    cost_time = getattr(response, "cost_time")
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
    print(entry.request_time)
    entry.response_header = str(response._headers)
    entry.size = len(entry.body)
    entry.status_code = 500
    entry.save()
