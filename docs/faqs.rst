
FAQs
====

This document contains frequently asked questions about the project. 

How can I ask questions?
-------------------------
If you have a question that is not answered here, `please open an issue on GitHub <https://github.com/adrian-gallus/lazy-signals-python/issues/new>`_.

Who is this library for?
------------------------
This library is designed for developers who need an easy-to-use reactive programming model in their Python applications.
It is tailored towards GUI applications, game development, and data processing pipelines.

Isn't this just the Observer Pattern?
-------------------------------------
.. _observer-pattern:

No.
The Observer Pattern is a behvioural design pattern that allows objects to  subscribe to events and be notified when those events occur.
While this is used internally, a user of this library is not supposed to make explicit subscriptions.
