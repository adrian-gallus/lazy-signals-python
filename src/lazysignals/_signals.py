
# Copyright 2025, Adrian Gallus

# TODO write tests
# TODO add type hints

# TODO make threadsafe and async
# TODO allow manual dependency declaration
# TODO an effect should be able to make _atomic_ updates (update multiple signals at once); just run effects to completion before propagating changes?
# TODO make a debugging tool to view the dependency tree
# TODO provide _eager_ and _lazy_ signals to compensate overhead; benchmark

# NOTE an effect may become dirty again if there are cyclic dependnecies through side effects; hence we must reset the flag before running the effect

from ._utils import SingletonMeta, is_added


class Updated(metaclass=SingletonMeta):
    """
    A singleton to track the events that have been updated.
    """

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
    """
    A singleton to track the signals that have been accessed while executing an effect.
    """

    def __init__(self):
        self._effects = []

    @property
    def is_set(self):
        return len(self._effects) > 0

    def get(self, dependency):
        effect = self._effects[-1]
        fresh = effect.add_dependency(dependency)
        return fresh, effect
    
    def enter(self, effect):
        self._effects.append(effect)

    def leave(self):
        self._effects.pop()


class Effect():
    """A container to hold an effect function."""

    def __init__(self, fn):
        self._dependencies = set()
        self._fn = fn

    def add_dependency(self, dependency):
        return is_added(self._dependencies, dependency)

    def update(self):
        updated = Updated()
        if updated.submit(self):
            Dependent().enter(self)
            try:
                return self._fn()
            except:
                raise
            finally:
                Dependent().leave()


# TODO hide .value by making the class a decorator
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
        """
        :getter: gets the current value, registering the current effect as a dependent
        :setter: sets the current value, notifying all dependent effects if it changed
        """

        dependent = Dependent()
        if dependent.is_set:
            fresh, effect = dependent.get(self)
            if fresh: # avoid duplicates
                self._dependents.append(effect)

        return self._value

    @value.setter
    def value(self, value):
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


def effect(fn):
    """
    Run ``fn()`` whenever (relevant) state changes.

    :param fn: The function to run on state changes.
    :returns: The return value of ``fn()``.

    .. tip::
        Use as a function decorator.
    """
    return Effect(fn).update()


def derived(fn):
    """
    Define a new signal whose value is computed by ``fn()``.
    
    :param fn: A function to compute the value from.
    :returns: A new ``Signal``.

    .. tip::
        Use as a function decorator.
    """
    
    derived = Signal()
    
    @effect
    def update():
        derived.value = fn()
    
    return derived

