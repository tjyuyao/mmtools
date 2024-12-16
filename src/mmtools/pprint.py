from rich.pretty import pprint as _rich_pprint   


class _direct_print_no_repr(str):
    def __repr__(self):
        return self

# (types, repr)
custom_repr = [
    ((int, float, str), _direct_print_no_repr),
]

# (types)
custom_list = [list, tuple]

# (types, items)
custom_dict = [
    ((dict,), "items")
]


def pprint(x):

    def _pprint(_x):
        
        for types, func in custom_repr:
            if isinstance(_x, types):
                return func(_x)

        raise TypeError

    _rich_pprint(_apply(x, _pprint))


def _apply(x, f):

    if isinstance(x, tuple(custom_list)):
        if len(x) and sum([isinstance(xi, (str, int, float)) for xi in x]) == len(x):
            return _direct_print_no_repr(f"[{repr(x[0])}, ...]")
        return x.__class__([_apply(xi, f) for xi in x])

    if not isinstance(x, dict):
        if _has_method(x, "to_dict"):
            x = x.to_dict()
        if _has_method(x, "as_dict"):
            x = x.as_dict()
        if _has_method(x, "items"):
            x = dict(x)

    if isinstance(x, dict):
        return {k: _apply(v, f) for k, v in x.items()}

    try:
        return f(x)
    except TypeError:
        return _direct_print_no_repr(f"Unknown type: <{type(x).__name__}>")
    except Exception as e:
        return _direct_print_no_repr(f"<{e}>")


def _has_method(obj, methodname) -> bool:
    return getattr(getattr(obj, methodname, None), "__call__", False) is not False


try:
    from torch import Tensor
    def _pprint_tensor(x):
        dtype = str(x.dtype).replace("torch.", "")
        return _direct_print_no_repr(f"Tensor({tuple(x.shape)}, {dtype})")
    custom_repr.append((Tensor, _pprint_tensor))
except ImportError:
    pass


try:
    from numpy import ndarray
    def _pprint_ndarray(x):
        dtype = str(x.dtype)
        return _direct_print_no_repr(f"ndarray({tuple(x.shape)}, {dtype})")
    custom_repr.append((ndarray, _pprint_ndarray))
except ImportError:
    pass
