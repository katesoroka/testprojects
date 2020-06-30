from datetime import datetime



def message_decorator(func):
    def wrapper():
        if 7 <= datetime.now().hour < 22:
            func('day')
        else:
            func()
    return wrapper

@message_decorator
def say_whee(text='say bla bla'):
    print(text)



import functools

def do_twice(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        func(*args, **kwargs)
        return func(*args, **kwargs)
    return wrapper

@do_twice
def say_whee(text):
    print(text)


# say_whee('aa')
#

import time

def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()  # 1
        value = func(*args, **kwargs)
        end_time = time.perf_counter()  # 2
        run_time = end_time - start_time  # 3
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value
    return wrapper_timer


@timer
def waste_some_time(num_times):
    for _ in range(num_times):
        sum([i**2 for i in range(10000)])


def debug(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"Calling {func.__name__} ({signature})")
        value = func(*args, **kwargs)
        print(f"{func.__name__!r} returned {value!r}")
        return value
    return wrapper



@debug
def make_greeting(name, age=None):
    if age is None:
        return f"Howdy {name}!"
    else:
        return f"Whoa {name}! {age} already!"

import random
PLUGINS = dict()

def register(func):
    """Register a function as a plugin"""
    PLUGINS[func.__name__] = func
    return func


@register
def say_hello(name):
    return f"Hello {name}"

@register
def be_awesome(name):
    return f"Yo {name}, together we are the awesomest!"

def randomly_greet(name):
    greeter, greeter_func = random.choice(list(PLUGINS.items()))
    print(f"Using {greeter!r}")
    print(greeter_func(name))


## flask examples

from flask import Flask, g, request, redirect, url_for
import functools
app = Flask(__name__)
def login_required(func):
    @functools.wraps(func)
    def wrapper_login_required(*args, **kwargs):
        if g.user in None:
            return redirect(url_for("login", next=request.url))
        return func(*args, **kwargs)
    return wrapper_login_required


#
#
# def repeat(num_times):
#     def decorator_repeat(func):
#         @functools.wraps(func)
#         def wrapper(*args, **kwargs):
#             for _ in range(num_times):
#                 value = func(*args, **kwargs)
#             return value
#         return wrapper
#     return decorator_repeat

def repeat(num_times, bla):
    def var_dec(func):
        def wrapper(*args, **kwargs):
            for _ in range(num_times):
                value = func(*args, **kwargs)
            return value
        print(bla)
        return wrapper
    return var_dec

@repeat(num_times=4, bla='aha')
def greet(name):
    print(f"Hello {name}")

def repeat(_func=None, *, num_times=2):
    def dec_rep(func):
        @functools.wraps(func)
        def wrap_rep(*args, **kwargs):
            for _ in range(num_times):
                value = func(*args, **kwargs)
            return value
        return wrap_rep
    if _func is None:
        return dec_rep
    else:
        return dec_rep(_func)

def count_calls(func):
    @functools.wraps(func)
    def wrapper_count_calls(*args, **kwargs):
        wrapper_count_calls.num_calls += 1
        print(f"Call {wrapper_count_calls.num_calls} of {func.__name__!r}")
        return func(*args, **kwargs)
    wrapper_count_calls.num_calls = 0
    return wrapper_count_calls


