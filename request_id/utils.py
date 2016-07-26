def aslist_cronly(value):
    return filter(None, [x.strip() for x in value.splitlines()])

def aslist(value, flatten=True):
    """
    Return a list of strings, separating the input based on newlines and,
    if ``flatten`` is ``True`` (the default), also split on spaces within
    each line.

    """
    values = aslist_cronly(value)
    if not flatten:
        return values
    return [sv for val in values for sv in val.split()]
