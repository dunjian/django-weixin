#!coding: utf-8
import time
from datetime import datetime

from django.utils.module_loading import autodiscover_modules

import signals


autodiscover_modules("signalproc")


class TrackingMiddleware(object):
    def process_request(self, request):
        setattr(request, "timestamp", time.time())
        signals.sig_tracking_request.send(sender=self, request=request)

    def process_response(self, request, response):
        signals.sig_tracking_before_tracking.send(sender=self, request=request, response=response)
        now = time.time()
        request_timestamp = getattr(request, "timestamp", now)
        cost_time = int(1000 * (now - request_timestamp))
        setattr(response, "cost_time", cost_time)

        response_status_code = response.status_code
        sig = getattr(signals, "sig_%s" % response_status_code, None)
        if sig is not None:
            sig.send(sender=self, request=request, response=response)

        signals.sig_tracking_after_tracking.send(sender=self, request=request, response=response)
        return response
