
# Copyright 2025, Adrian Gallus

# TODO make async and lazy


dependent = None


class Signal:

    def __init__(self, value=None):
        self._value = value
        self._subscribers = set()

    @property
    def value(self):
        if dependent is not None:
            self._subscribers.add(dependent)
        return self._value

    @value.setter
    def value(self, value):
        self.set(value)

    def set(self, value):
        self._value = value
        for subscriber in self._subscribers:
            subscriber()


# NOTE may be used as decorator
def effect(fn):
    dependent = fn
    fn()
    dependent = None


# NOTE may be used as decorator, similar to @property
def derived(fn):
    derived = Signal()
    effect(lambda: derived.set(fn()))
    return derived



