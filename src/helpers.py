from datetime import datetime
from .globals import Mutable


def asrt(cond, msg, fallback=None):
    if not cond and (Mutable.g_args.node or Mutable.g_args.miner):
        raise Exception(msg)
    if cond:
        return fallback


def asrt_not(cond, msg, fallback=None):
    if cond and (Mutable.g_args.node or Mutable.g_args.miner):
        raise Exception(msg)
    if not cond:
        return fallback


def log(txt):
    print(f'{str(datetime.now())[:-7]} >> {txt}')


def cli(msg='enter your query'):
    log(msg)

    while True:
        q = input(msg + ' [or enter exit]\n')
        if q == "exit":
            break
        yield q
