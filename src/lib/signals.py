
# Copyright 2025, Adrian Gallus

# TODO make lazy, threadsafe, and async


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Node():

    def __init__(self, fn):
        self._dependencies = set()
        self._fn = fn

    def add_dependency(self, dependency):
        self._dependencies.add(dependency)

    def notify(self):
        effect(self._fn, node=self)


class Dependent(metaclass=SingletonMeta):

    def __init__(self):
        self._values = []

    def pop(self):
        self._values.pop()

    def push(self, value, node):
        self._values.append(node if node else Node(value))

    @property
    def is_set(self):
        return len(self._values) > 0

    def get(self, dependency):
        value = self._values[-1]
        value.add_dependency(dependency)
        return value


class Signal:

    def __init__(self, value=None):
        self._value = value
        self._subscribers = set()

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"Signal({self._value})"

    @property
    def value(self):
        dependent = Dependent()
        if dependent.is_set:
            self._subscribers.add(dependent.get(self))
        return self._value

    @value.setter
    def value(self, value):
        self.set(value)

    def set(self, value):
        self._value = value
        exceptions = []
        for subscriber in list(self._subscribers):
            try:
                subscriber.notify()
            except Exception as e:
                exceptions.append(e)
        if len(exceptions) > 0:
            raise Exception(*exceptions)


# NOTE may be used as decorator
def effect(fn, node=None):
    Dependent().push(fn, node)
    try:
        fn()
    except:
        raise
    finally:
        Dependent().pop()


# NOTE may be used as decorator, similar to @property
def derived(fn):
    derived = Signal()
    effect(lambda: derived.set(fn()))
    return derived



