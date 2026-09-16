#fonctions used in the lab 1notebook with documentation


def string_in_keys(d: dict, s: str):
    """Return 123 if the key ``s`` is absent from ``d``, otherwise return None.

    Parameters
    ----------
    d : dict
        The dictionary to search.
    s : str
        The key to look up.

    Returns
    -------
    int or None
        123 if ``s`` is not a key of ``d``, None otherwise (implicit return).

    Examples
    --------
    >>> string_in_keys({"a": 1, "b": 2}, "a")
    >>> string_in_keys({"a": 1, "b": 2}, "z")
    123
    """
    if s not in d.keys():
        return 123


def make_fiz_buzz(L: list) -> list:
    """Apply a FizzBuzz-like rule to a list and return the transformed list.

    For each element at index ``i`` in ``L``:

    - append ``"fizbuz"`` if the element is divisible by both 5 and 7,
    - append ``"fiz"``    if the element is divisible by 5 only,
    - append ``"buz"``    if the element is divisible by 7 only,
    - append ``i`` (the index) otherwise.

    Parameters
    ----------
    L : list of int
        Input list of integers.

    Returns
    -------
    list
        A list of the same length as ``L`` where each entry is one of
        ``"fizbuz"``, ``"fiz"``, ``"buz"``, or the original index.

    Examples
    --------
    >>> make_fiz_buzz([2, 1, 3, 31, 35, 20, 70, 132, 144, 49])
    [0, 1, 2, 3, 'fizbuz', 'fiz', 'fizbuz', 7, 8, 'buz']
    >>> make_fiz_buzz([35, 5, 7, 4])
    ['fizbuz', 'fiz', 'buz', 3]
    >>> make_fiz_buzz([])
    []
    """
    fizbee = []
    for i in range(len(L)):
        if L[i] % 5 == 0 and L[i] % 7 == 0:
            fizbee.append("fizbuz")
        elif L[i] % 5 == 0:
            fizbee.append("fiz")
        elif L[i] % 7 == 0:
            fizbee.append("buz")
        else:
            fizbee.append(i)
    return fizbee


def describe_price(fruit: str, quantity: int, price: float) -> str:
    """Format a human-readable price description for a given fruit purchase.

    The output string follows the pattern::

        <quantity> <fruit>[s] cost[s] $<price>

    where:
    - ``fruit`` is pluralised (``"s"`` appended) when ``quantity != 1``,
    - ``"costs"`` is used for a single item, ``"cost"`` otherwise,
    - ``price`` is rounded to two decimal places.

    Parameters
    ----------
    fruit : str
        Name of the fruit (singular form).
    quantity : int
        Number of fruits purchased.
    price : float
        Total price in dollars (displayed rounded to the nearest cent).

    Returns
    -------
    str
        Formatted price string.

    Examples
    --------
    >>> describe_price("avocado", 1, 1.50)
    '1 avocado costs $1.50'
    >>> describe_price("avocado", 2, 1.8912392e4)
    '2 avocados cost $18912.39'
    >>> describe_price("mango", 3, 1.999)
    '3 mangos cost $2.00'
    """
    fruit_name = fruit if quantity == 1 else f"{fruit}s"
    verb = "costs" if quantity == 1 else "cost"
    return f"{quantity} {fruit_name} {verb} ${price:.2f}"


def is_unique(x: list) -> bool:
    """Return True if all elements of ``x`` are distinct, False otherwise.

    This implementation relies on the fact that a ``set`` discards duplicates:
    if the set is smaller than the original list, at least one element appears
    more than once.

    Note
    ----
    Elements must be hashable (ints, strings, tuples, …). Lists-of-lists will
    raise a ``TypeError`` because lists are not hashable.

    Parameters
    ----------
    x : list
        The list to check. Elements must be hashable.

    Returns
    -------
    bool
        ``True`` if every element appears exactly once, ``False`` if any
        element is repeated.

    Examples
    --------
    >>> is_unique([1, 2, 3, 4])
    True
    >>> is_unique([1, 2, 3, 3])
    False
    >>> is_unique([])
    True
    """
    return len(x) == len(set(x))


def triangle_shape(height: int) -> str:
    """Return a string representation of an isoceles triangle of given height.

    Each row ``i`` (0-indexed from the top) contains:
    - ``height - i - 1`` leading spaces,
    - ``2 * i + 1`` ``'x'`` characters,
    - ``height - i - 1`` trailing spaces,
    - a newline character.

    All rows have the same total width (``2 * height - 1`` characters plus
    the newline), so the triangle is properly centred.

    Parameters
    ----------
    height : int
        Number of rows. Must be a non-negative integer.
        ``height=0`` returns an empty string.

    Returns
    -------
    str
        Multi-line string representing the triangle, with each line terminated
        by ``'\\n'``. Returns ``""`` when ``height`` is 0.

    Examples
    --------
    >>> triangle_shape(1)
    'x\\n'
    >>> triangle_shape(3)
    '  x  \\n xxx \\nxxxxx\\n'
    >>> triangle_shape(0)
    ''
    """
    if height == 0:
        return ""

    triangle = ""
    for i in range(height):
        stair = " " * (height - i - 1) + "x" * (2 * i + 1) + " " * (height - i - 1) + "\n"
        triangle += stair
    return triangle


def usefulness(course: str) -> None:
    """Print a message describing the usefulness of a course.

    Parameters
    ----------
    course : str
        Name of the course. The following courses have specific messages:
        ``"maths"`` and ``"python"`` are considered useful,
        ``"meditation"`` receives a positive response, and ``"magic"``
        receives a Hogwarts-related response.

    Returns
    -------
    None
        This function only prints a message and does not return a value.

    Examples
    --------
    >>> usefulness("maths")
    That is very useful!
    >>> usefulness("python")
    That is very useful!
    >>> usefulness("meditation")
    How nice
    >>> usefulness("magic")
    You're not at Hogwarts
    >>> usefulness("history")
    What is this COURSE?
    """
    if course == "maths" or course == "python":
        print("That is very useful!")
    elif course == "meditation":
        print("How nice")
    elif course == "magic":
        print("You're not at Hogwarts")
    else:
        print("What is this COURSE?")
    return None
