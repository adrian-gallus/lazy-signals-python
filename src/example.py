
from lib.signals import Signal, effect, derived

s = Signal(1)

@derived
def t():
    return 2 * s.value

h = derived(lambda: t.value + 1)

@effect
def status():
    # NOTE this has no effect on update
    print(f"status: got {s=} and {h=}")


@effect
def logger():
    # NOTE this is called on each update
    print(f"logger: got {s.value=} and h =", h)

effect(lambda: print(f"with {t=}"))

print("set s = 3")
s.value = 3

try:
    @effect
    def exception():
        print("raising exception on t =", t)
        raise Exception("test")
except:
    pass

try:
    print("set s = 4")
    s.value = 4
except Exception as e:
    print("handling exception(s)", e)
