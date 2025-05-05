
# Copyright 2025, Adrian Gallus

# TODO make threadsafe and async
# TODO allow manual dependency declaration
# TODO an effect should be able to make _atomic_ updates (update multiple signals at once)
# TODO make a debugging tool to view the dependency tree
# TODO provide _eager_ and _lazy_ signals to compensate overhead; benchmark

# NOTE an effect may become dirty again if there are cyclic dependnecies through side effects; hence we must reset the flag before running the effect

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


# unfortunately the .add method does not return its effect
def is_added(s, x):
    if x not in s:
        s.add(x)
        return True
    return False


# avoid duplicate updates per signal propagation pass
class Updated(metaclass=SingletonMeta):

    def __init__(self):
        self._signals = set()
        self._updated = set()

    def enter_signal(self, signal):
        self._signals.add(signal)

    def leave_signal(self, signal):
        self._signals.remove(signal)
        # cleanup when all signales propagated
        if not self._signals:
            self._updated = set()

    def submit(self, updated):
        return is_added(self._updated, updated)


# run updates (but only once per change)
class Effect():

    def __init__(self, fn):
        self._dependencies = set()
        self._fn = fn

    def add_dependency(self, dependency):
        return is_added(self._dependencies, dependency)

    def update(self):
        updated = Updated()
        if updated.submit(self):
            effect(self._fn, effect=self)


class Dependent(metaclass=SingletonMeta):

    def __init__(self):
        self._effects = []

    def pop(self):
        self._effects.pop()

    def push(self, effect):
        self._effects.append(effect)

    @property
    def is_set(self):
        return len(self._effects) > 0

    def get(self, dependency):
        effect = self._effects[-1]
        fresh = effect.add_dependency(dependency)
        return fresh, effect


class Signal:

    def __init__(self, value=None):
        self._value = value
        self._dependents = [] # NOTE must preserve order (may use dict instead of list) to ensure that each (single) effect update happens only after all dependencies already updated

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"Signal({self._value})"

    @property
    def value(self):
        dependent = Dependent()
        if dependent.is_set:
            fresh, effect = dependent.get(self)
            if fresh: # avoid duplicates
                self._dependents.append(effect)
        return self._value

    @value.setter
    def value(self, value):
        self.set(value)

    # NOTE assignment `x.value = a` is not an expression, but `x.set(a)` is; this is useful for lambdas
    def set(self, value):
        if self._value == value:
            return
        self._value = value
        exceptions = []
        updated = Updated()
        updated.enter_signal(self)
        for dependent in list(self._dependents):
            try:
                dependent.update()
            except Exception as e:
                exceptions.append(e)
        updated.leave_signal(self)
        if len(exceptions) > 0:
            raise Exception(*exceptions)


# NOTE may be used as decorator
def effect(fn, effect=None):
    Dependent().push(effect or Effect(fn))
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



