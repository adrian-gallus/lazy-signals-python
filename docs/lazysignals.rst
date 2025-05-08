
Lazy Signals
============

In this library, there are `signals` and `effects`.
Signals are containers that hold a single value.
Effects are functions that are called when any signal they depend on changes its value.

.. warning::
   Read :ref:`this <observer-pattern>` if you came to the impression that the library just implements the observer pattern.


.. contents:: Table of Contents
   :depth: 2
   :local:
   :backlinks: none


Define Signals
--------------

There are two major ways to define a new signal:

1. Define a variable-style signal by using the :py:class:`Signal` constructor.
   You can pass in the initial value and update it by assigning to the :py:attr:`value` property.

2. Build a signal from others by using the :py:func:`func` decorator.
   You write a function that uses the :py:attr:`value` property of other signals to compute a live value.


Top Level Signals
~~~~~~~~~~~~~~~~~

.. autoclass:: lazysignals.Signal
   :no-index:
   :members:
   :undoc-members:

You can create a signal by calling the constructor.
Optionally, you can pass in the initial value.
An instance of this class very much behaves like a normal variable:
Simply use ``signal.value`` to access (get/set) its value.
You must wrap your variables in this class to make them reactive.

Example:
   .. code-block:: python

      from lazysignals import Signal

      s = Signal(0)   # create a signal with initial value 0
      print(s.value)  # prints '0'
      s.value = 1     # update the value
      print(s.value)  # prints '1'

.. tip::
   While python forbids assignments ``s.value = new_value`` in lambda expressions, you can use ``s.set(new_value)`` instead.
   So ``lambda: s.set(new_value)`` is a valid python expression.


Derived Signals
~~~~~~~~~~~~~~~

.. autofunction:: lazysignals.derived
   :no-index:

Internally, this just defines an effect to update the derived signal via the provided function.

Example:
   .. code-block:: python

      from lazysignals import Signal, derived

      s = Signal(0) # create a signal with initial value 0
      
      # compute `parity.value` via `s.value % 2`
      # `parity` now depends on `s`
      @derived
      def parity():
         return s.value % 2
      
      print(parity.value) # prints '0'
      s.value = 1 # update the value of `s` (not `parity`)
      print(parity.value) # prints '1'


.. note::
   You do not need to define dependencies manually.
   However, they are only detected when they lie in the active code path.
   This means that if you mention a signal ``s`` in the function ``fn`` but do not make use of ``s.value``, the dependency will not be detected.
   For example if we have two signals ``s`` and ``t`` where ``t.value`` evaluates to ``False`` and we let ``fn = lambda: None if t.value else s.value``, then ``t`` but not ``s`` will be tracked initially.
   If, ``t.value`` now changes to ``True``, causing an update call to ``fn`` for the derived signal, the new dependency on ``s`` will be recognized and respected down the line.

.. tip::
   Only those signals are recomputed that may actually change.
   We call this *lazy evaluation*.


Define Effects
--------------

.. autofunction:: lazysignals.effect
   :no-index:

The :py:func:`effect` decorator allows you to define a function that is called whenever one of the signals on which the decorated function depends changes.

Example:
   .. code-block:: python

      from lazysignals import Signal, derived

      s = Signal(0) # create a signal with initial value 0
      t = 0         # create a normal variable with initial value 0
      
      # define an effect that prints the value of `s` and `t`
      # immediately prints "0, 0"
      @effect
      def printer():
         print(f"{s.value}, {t}")
      
      s.value = 1 # prints "1, 0"
      t = 1       # does not print anything
      s.value = 1 # does not print anything
      s.value = 2 # prints "2, 1"

.. note::
   The function ``fn`` is called immediately when the effect is defined.
   Moreover, it is called whenever any of the signals it depends on changes its value.
   Because of lazy evaluation, it is not called on assignments to other signals or those who do not actually change a value.
   For obvious reasons, the effect is not called when variables change that are not defined as signals.

.. note::
   You do not need to define dependencies manually.
   However, as with derived signals, they are only detected when they lie in the active code path.

.. tip::
   You can use the :func:`effect` as a function decorator.
   But you can also use as a function call, for example, ``effect(lambda: print(s.value))``.
   The call returns the result of evaluating the function.


A Note on Exceptions
--------------------

Whenever exceptions are raised in a derived signal or effect, they are collected and raised at the end of the current signal propagation phase.
This exception takes the form of ``Exception(...list of raised exceptions...)``.
