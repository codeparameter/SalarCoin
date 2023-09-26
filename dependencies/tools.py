import hashlib
import json
import random
import time

import ecdsa
from faker import Faker
from concurrent.futures import ThreadPoolExecutor

fake = Faker()
all_ips = set()


def fake_ip() -> str:
    ip = fake.ipv4()
    all_ips.add(ip)
    return fake_ip() if ip in all_ips else ip


# noinspection PyBroadException
def nxt(itr):
    try:
        return next(itr)
    except Exception:
        return None


def rem_rand_choice(itr):
    selected = random.choice(itr)
    itr.remove(selected)
    yield selected


def unique_rand_choice(itr):
    assert len(itr) == len(set(itr)), 'initial iterable must have unique items'
    yield from rem_rand_choice(itr[:])


def sort_dict(d: dict, fn, reverse=False):
    return dict(sorted(d.items(), key=lambda i: fn(i[1]), reverse=reverse))


def ripemd160(data):
    ripemd160_b = hashlib.new('ripemd160')
    ripemd160_b.update(data)
    return ripemd160_b.digest()


def dict_to_bytes(dct):
    return json.dumps(dct).encode()


def timestamp():
    return int(time.time())


def fn_tuple(fn, *args, **kwargs):
    fn(*args, **kwargs)


def fn_chain(fn_tuples: tuple):
    for ft in fn_tuples:
        fn_tuple(ft[0], *ft[1:-1], **ft[-1])


"""
def test(*args, **kwargs):
    print(args)
    print(kwargs)


fn_chain((
    (test, '1', '2', {'a': 3, 'b': 4}),
    (test, {}),
))
"""


def multi_thread_chain(fn_tuples: tuple):
    with ThreadPoolExecutor() as executor:
        for ft in fn_tuples:
            executor.submit(ft[0], args=ft[1:-1], kwargs=ft[-1])


def single_thread_chain(fn_tuples: tuple):
    for ft in fn_tuples:
        with ThreadPoolExecutor() as executor:
            executor.submit(ft[0], args=ft[1:-1], kwargs=ft[-1])


"""
def asrt2(cond, msg):
    if not cond:
        raise Exception(msg)
    if cond:
        return fn_chain


def asrt(cond, msg, fallback=None):
    if not cond:
        raise Exception(msg)
    if cond:
        return fallback
"""


def chain(chain_fallback):
    def inner(fn):
        def wrapper(*args, **kwargs):
            fn(*args, **kwargs)
            return chain_fallback

        return wrapper

    return inner


"""
@chain(fn_chain)
def test1(msg):
    print(msg)


def test2(msg):
    print(msg)


test1('1')((
    (test2, '2', {}),
    (test2, '3', {}),
    (test2, '4', {}),
))
"""
