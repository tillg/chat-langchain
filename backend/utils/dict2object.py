
def dict2object(d):
    """
    Convert a dictionary to an object, including nested dictionaries and arrays.
    """
    if not isinstance(d, dict):
        return d

    class C:
        pass
    o = C()
    for k, v in d.items():
        if isinstance(v, dict):
            setattr(o, k, dict2object(v))
        elif isinstance(v, list):
            setattr(o, k, [dict2object(i) if isinstance(
                i, dict) else i for i in v])
        else:
            setattr(o, k, v)
    return o
