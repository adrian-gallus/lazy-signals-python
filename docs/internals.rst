
Internal Mechanics
==================

The library resides on three principles: dependency detection via a singleton, the observer pattern, and lazy evaluation via memoization.


Dependency Detection
--------------------

When an effect runs, it registers itself with the ``Dependent`` singleton.
While evaluating its payload function ``fn``, if it accesses any signal values through the ``signal.value`` getter, those signals register the effect as a subscriber.
After the effect finishes running, it removes itself from the ``Dependent`` singleton to avoid creating unnecessary dependencies.

The same happens when a derived signal is created.
Indeed, derived signals are just effects, where the payload function evaluates the defining function and assigns its result to the derived signal.


Lazy Evaluation
---------------

When the ``signal.value`` setter is called, it checks if the new value is different from the stored one. If it is, the new value is stored, and all dependents are notified of the change.

The subscribed effects register themselves with the ``Updated`` singleton.
They only call their payload function ``fn`` if they were not registered before.
Since notifications proceed in a depth-first manner, this ensures that effects are only called once after all their dependencies have been updated.
This also implies that the order of definition matters, and cyclic dependencies are not allowed.
Once all changes are propagated and all dependent effects have run, the effects must be ready to run again.
To this end, the ``Updated`` singleton also tracks all changing signals and resets its registry after they have notified all their dependents.
