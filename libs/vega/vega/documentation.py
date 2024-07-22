import functools


def inherit_docstring_from(parent_class):
    """
    A decorator to inherit the docstring from a method in a parent class.

    This decorator is used to copy the docstring from a method in the parent class to a method in the
    child class. It helps to avoid redundant documentation and ensures that the child method has the
    same docstring as the parent method.

    Args:
        parent_class (type): The parent class from which to inherit the docstring.

    Returns:
        function: A decorator that copies the docstring from the parent method to the child method.

    Example Usage:
        class BaseClass:
            def some_method(self):
                \"\"\"
                This is the docstring for some_method in BaseClass.
                \"\"\"
                pass

        class DerivedClass(BaseClass):
            @inherit_docstring_from(BaseClass)
            def some_method(self):
                # This method will inherit the docstring from BaseClass.some_method
                pass

        # You can check the docstring to see if it was inherited
        print(DerivedClass.some_method.__doc__)
    """
    def decorator(func):
        parent_method = getattr(parent_class, func.__name__, None)
        if parent_method and parent_method.__doc__:
            func.__doc__ = parent_method.__doc__
        return func
    return decorator
