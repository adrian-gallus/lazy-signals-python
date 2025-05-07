
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
    """
    Adds an element to a set and returns if it was not already present.
    
    :param: ``s``: The set to add the element to.
    :param: ``x``: The element to add.
    :returns: ``True`` if ``x`` was not in ``s``, ``False`` otherwise.
    """
    if x not in s:
        s.add(x)
        return True
    return False


# avoid duplicate updates per signal propagation pass
class Updated(metaclass=SingletonMeta):

    def __init__(self):
        self._signals = set()
        self._updated = set()

    def enter(self, signal):
        self._signals.add(signal)

    def leave(self, signal):
        self._signals.remove(signal)
        # cleanup when all signales propagated
        if not self._signals:
            self._updated = set()

    def submit(self, updated):
        if self._signals:
            return is_added(self._updated, updated)
        return True


class Dependent(metaclass=SingletonMeta):

    def __init__(self):
        self._effects = []

    @property
    def is_set(self):
        return len(self._effects) > 0

    def get(self, dependency):
        effect = self._effects[-1]
        fresh = effect.add_dependency(dependency)
        return fresh, effect
    
    def pop(self):
        self._effects.pop()

    def push(self, effect):
        self._effects.append(effect)


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
            Dependent().push(self)
            try:
                return self._fn()
            except:
                raise
            finally:
                Dependent().pop()


class Signal:
    """A container to hold a reactive value."""

    def __init__(self, value=None):
        self._value = value
        self._dependents = [] # NOTE must preserve order (may use dict instead of list) to ensure that each (single) effect update happens only after all dependencies already updated

    def __str__(self):
        """get a reactive string representation of the contained value"""
        return str(self.value)

    def __repr__(self):
        """get a (nonreactive) string representation of the container"""
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
        updated.enter(self)
        for dependent in list(self._dependents):
            try:
                dependent.update()
            except Exception as e:
                exceptions.append(e)
        updated.leave(self)
        if len(exceptions) > 0:
            raise Exception(*exceptions)


# NOTE may be used as decorator
def effect(fn):
    """
    Run ``fn()`` whenever (relevant) state changes.

    :param: ``fn``: The function to run on state changes.
    :returns: The return value of ``fn()``.
    """
    return Effect(fn).update()


# NOTE may be used as decorator, similar to @property
def derived(fn):
    """
    Define a new signal whose value is computed by ``fn()``.
    
    :param: ``fn``: A function without arguments that returns a value.
    :returns: A new ``Signal``.
    """
    derived = Signal()
    effect(lambda: derived.set(fn()))
    return derived

