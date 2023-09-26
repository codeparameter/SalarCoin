import ecdsa

from dependencies.tools import ripemd160
from src.wallet.keyobject import key_from_string, verify


def DUP(stack):
    stack.append(stack[-1])


def HASH160(stack):
    res = ripemd160(stack.pop())
    stack.append(res)


def EQUAL_VERIFY(stack):
    stack.append(stack.pop() == stack.pop())


def cs(stack):
    vk: ecdsa.VerifyingKey = key_from_string(ecdsa.VerifyingKey, stack.pop())
    sig = stack.pop()
    msg = stack.pop()
    stack.append(verify(vk, sig, msg))


def CHECK_SIG(stack):
    one = stack.pop()
    if isinstance(one, bool):
        if not one:
            stack.pop()
            stack.pop()
            stack.append(False)
            return
        cs(stack)
    stack.append(one)
    cs(stack)


def run_script(code: tuple):
    stack = []
    for state in code:
        if callable(state):
            state(stack)
        else:
            stack.append(state)
    return stack.pop()


scripts = {
    'DUP': DUP,
    'HASH160': HASH160,
    'EQUAL_VERIFY': EQUAL_VERIFY,
    'CHECK_SIG': CHECK_SIG,
}


def script(code: str):
    code = code.split(' ')
    code = tuple((scripts[state] if state in scripts else state for state in code))
    return run_script(code)
