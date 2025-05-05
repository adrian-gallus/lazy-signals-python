
# Lazy Signals 🪢

`lazysignals` is a python library to run effects on state changes. It employs dependency discovery and is lazy. It is conceptually inspired by Signal in JavaScript.

## Example

The framework runs relevant effects whenever some state changes:

define a new signal `s`, holding the initial value `1`

    s = Signal(1)

derive a signal that checks the parity of `s`

    p = derived(lambda: s.value % 2 == 0)

log the parity of `s` to the console

    effect(lambda: print(f"parity:", "even" if p.value else "odd"))

perform some updates to `s`

    s.value = 1  # no change, no output
    s.value = 2  # output: "parity: even"
    s.value = 3  # output: "parity: odd"
    s.value = 5  # no change, no output
    s.value = 6  # output: "parity: even"

Have a look at `example.py` for more; run with `pipenv install` (to locally install this library) and `pipenv run example`.
