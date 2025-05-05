
# Copyright 2025, Adrian Gallus

# TODO make async and lazy


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Dependent(metaclass=SingletonMeta):

    def __init__(self):
        self.reset()

    def reset(self):
        self._value = None

    def set(self, value):
        assert not self.is_set
        self._value = value

    @property
    def is_set(self):
        return self._value is not None

    @property
    def current(self):
        return self._value


class Signal:

    def __init__(self, value=None):
        self._value = value
        self._subscribers = set()

    @property
    def value(self):
        dependent = Dependent()
        if dependent.is_set:
            self._subscribers.add(dependent.current)
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



