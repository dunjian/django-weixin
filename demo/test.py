#!coding: utf-8
__author__ = 'zkchen'


def my_dec1(func):
    def inner(arg):
        return func("hello1", arg)
    return inner


def my_dec2(func):
    def inner(arg):
        return func("hello2", arg)
    return inner


def my_dec(arg):
    if arg == 1:
        return my_dec1
    else:
        return my_dec2


def replace(func):
    def inner():
        print("replace ...")
    return inner


@replace
def my_func(word, data):
    print(word)
    print(data)
    return "data"


if __name__ == "__main__":
    ret = my_func()
    print(ret)
