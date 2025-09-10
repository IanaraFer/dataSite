def assert_equal(actual, expected, message="Values are not equal"):
    """
    Custom assertion to check if two values are equal.
    
    Args:
        actual: The actual value.
        expected: The expected value.
        message: Optional message to display on failure.
    
    Raises:
        AssertionError: If the actual value does not equal the expected value.
    """
    assert actual == expected, message


def assert_in(item, collection, message="Item not found in collection"):
    """
    Custom assertion to check if an item is in a collection.
    
    Args:
        item: The item to check.
        collection: The collection to check against.
        message: Optional message to display on failure.
    
    Raises:
        AssertionError: If the item is not found in the collection.
    """
    assert item in collection, message


def assert_is_instance(obj, cls, message="Object is not an instance of the expected class"):
    """
    Custom assertion to check if an object is an instance of a class.
    
    Args:
        obj: The object to check.
        cls: The expected class.
        message: Optional message to display on failure.
    
    Raises:
        AssertionError: If the object is not an instance of the expected class.
    """
    assert isinstance(obj, cls), message


def assert_raises(exception, func, *args, **kwargs):
    """
    Custom assertion to check if a specific exception is raised by a function.
    
    Args:
        exception: The expected exception class.
        func: The function to call.
        *args: Positional arguments to pass to the function.
        **kwargs: Keyword arguments to pass to the function.
    
    Raises:
        AssertionError: If the expected exception is not raised.
    """
    try:
        func(*args, **kwargs)
    except exception:
        return  # Expected exception raised
    except Exception as e:
        raise AssertionError(f"Expected {exception.__name__}, but got {type(e).__name__}") from e
    raise AssertionError(f"Expected {exception.__name__} was not raised")