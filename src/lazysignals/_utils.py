
# Copyright 2025, Adrian Gallus


class SingletonMeta(type):
    """
    A metaclass for creating singleton classes.

    This metaclass ensures that only one instance of a class is created, and that all subsequent calls to the constructor return the same instance.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Create and store a new instance of the class if it doesn't exist yet, or return the existing instance.
        """

        if cls not in cls._instances:
            # create a new instance
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        
        return cls._instances[cls]


# unfortunately the set.add method does not return its effect
def is_added(s, x):
    """
    Adds an element to a set and returns if it was not already present.
    
    :param s: The set to add the element to.
    :param x: The element to add.
    :returns: ``True`` if ``x`` was not in ``s``, ``False`` otherwise.
    """

    if x not in s:
        s.add(x)
        return True
    return False
