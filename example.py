
from lazysignals import *

### BASICS

print()
s = Signal(1)

@effect
def logger1():
    # NOTE this is called on each update
    print(f"logger 1: got {s.value=}")

@effect
def logger2():
    # NOTE this is called on each update
    print(f"logger 2: got s={s}")

@effect
def logger3():
    # NOTE this is NOT called on updates
    print(f"logger 3: got {s=}")

# NOTE this is NOT called on updates
print(f"logger 4: got s={s}")

s.value = 2
print()

### LAZYNESS

print()
s = Signal(1)
effect(lambda: print(f"update: {s.value=}"))

p = derived(lambda: s.value % 2 == 0)

@effect
def parity():
    # NOTE this is called on each update
    print(f"parity of s:", "even" if p.value else "odd")

s.value = 3 # no change
s.value = 2 # change to even
s.value = 3 # change to odd
s.value = 5 # no change
s.value = 6 # change to even
print()

### DECORATORS, CHAINS

print()
s = Signal(1)
effect(lambda: print(f"update: {s.value=}"))

@derived
def t():
    return 2 * s.value

h = derived(lambda: t.value + 1)

effect(lambda: print(f"got {h=}"))

@effect
def logger():
    # NOTE this should only emit once per update (although it has multiple dependencies)
    print(f"logger: got {s.value=}, {h.value=}")

s.value = 2
s.value = 3
print()

### EXCEPTIONS

print()
s = Signal(1)
effect(lambda: print(f"update: {s.value=}"))

try:
    @effect
    def exception():
        raise Exception(f"on s={s}")
except:
    pass

try:
    s.value = 2
except Exception as e:
    print("handling exception(s)", e)

print()
