
"""
A library that allows you to run effects whenever state changes.
It employs dependency discovery and updates are lazy.
"""

from ._signals import Signal, effect, derived
__all__ = ["Signal", "effect", "derived"]
