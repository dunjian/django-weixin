#!coding:utf-8
__author__ = 'akun'


import time
from django.shortcuts import render
from django.views.decorators import csrf


@csrf.csrf_exempt
def home(request):
    time.sleep(5)
    print(request.method)
    print("---------post----------")
    print(request.POST)
    try:
        print(request.POST['go'])
    except KeyError:
        print("key err")
    print("------get----------")
    print(request.GET)
    print("------------body--------")
    print("<%s>" % request.body)
    return render(request, "home.html", {})
