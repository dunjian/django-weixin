#!coding=utf-8
import django.dispatch

# msg signal
wxsignal_text = django.dispatch.Signal(providing_args=['msg'])

wxsignal_image = django.dispatch.Signal(providing_args=['msg'])

wxsignal_voice = django.dispatch.Signal(providing_args=['msg'])

wxsignal_video = django.dispatch.Signal(providing_args=['msg'])

wxsignal_location = django.dispatch.Signal(providing_args=['msg'])

wxsignal_link = django.dispatch.Signal(providing_args=['msg'])


# event signal
wxsignal_click_event = django.dispatch.Signal(providing_args=['msg'])

wxsignal_view_event = django.dispatch.Signal(providing_args=['msg'])

wxsignal_subscribe_event = django.dispatch.Signal(providing_args=['msg'])

wxsignal_unsubscribe_event = django.dispatch.Signal(providing_args=['msg'])

wxsignal_location_event = django.dispatch.Signal(providing_args=['msg'])

wxsignal_scan_event = django.dispatch.Signal(providing_args=['msg'])


