
Lazy Signals
============

This is a python library to run effects on value changes. It employs dependency discovery and is lazy. It is conceptually inspired by Signal in JavaScript.


.. toctree::
   :hidden:
   :maxdepth: 1

   library

.. contents:: Table of Contents
   :depth: 1
   :local:
   :backlinks: none


Example
-------

First, define a new signal ``s``, holding the initial value ``1``:

.. code-block:: python

    s = Signal(1)

Next, derive a signal that checks the parity of ``s``:

.. code-block:: python

    p = derived(lambda: s.value % 2 == 0)

Let us log the parity ``p`` to the console:

.. code-block:: python

    effect(lambda: print(f"parity:", "even" if p.value else "odd"))

Finally, perform some updates to ``s``:

.. code-block:: python

    s.value = 1  # no change (s.value was 1 already), no output
    s.value = 2  # output: "parity: even"
    s.value = 4  # output: "parity: odd"
    s.value = 5  # no change (p.value was False already), no output
    s.value = 6  # output: "parity: even"

Note how the effect only ran for those changes that mattered.

