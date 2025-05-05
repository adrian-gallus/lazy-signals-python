
from lib.signals import Signal, effect, derived

s = Signal(1)

@derived
def t():
    return 2 * s.value

h = derived(lambda: t.value + 1)

@effect
def logger():
    print("got s =", s.value, "and h =", h.value)

effect(lambda: print("with t =", t.value))

print("set s = 3")
s.value = 3

print("set s = 4")
s.value = 4

