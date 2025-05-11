
# Lazy Signals 🪢

[![GitHub](https://img.shields.io/github/license/adrian-gallus/lazy-signals-python)](https://github.com/adrian-gallus/lazy-signals-python)
[![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/adrian-gallus/lazy-signals-python/release.yaml)](https://github.com/adrian-gallus/lazy-signals-python)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/lazy-signals)](https://pypi.org/project/lazy-signals/)
[![PyPI - Version](https://img.shields.io/pypi/v/lazy-signals)](https://pypi.org/project/lazy-signals/)

`lazysignals` is a Python library that runs effects whenever state changes. It employs dependency discovery and updates are lazy. The library is conceptually inspired by [signals](https://github.com/tc39/proposal-signals) in JavaScript.

Please checkout our latest [documentation](https://adrian-gallus.github.io/lazy-signals-python/).

## Example

The framework runs relevant effects whenever some state changes:

define a new signal `s`, holding the initial value `1`

    s = Signal(1)

derive a signal that checks the parity of `s`

    p = derived(lambda: s.value % 2 == 0)

log the parity `p` to the console

    effect(lambda: print(f"parity:", "even" if p.value else "odd"))

perform some updates to `s`

    s.value = 1  # no change, no output
    s.value = 2  # output: "parity: even"
    s.value = 3  # output: "parity: odd"
    s.value = 5  # no change, no output
    s.value = 6  # output: "parity: even"

Have a look at `example.py` for more; run with `pipenv install` (to locally install this library) and `pipenv run example`.
