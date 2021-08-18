"""Utility functions
"""

import json
from collections import Iterable
from collections.abc import Mapping


def merge_dict(d, u):
    """Add u's keys to d. Override key in d if existing.
    Similar to JavaScript's Object.assign.
    """
    return {
        **d,
        **{
            key: merge_dict(d.get(key, {}), value)
                 if isinstance(val, Mapping)
                 else val
            for key, val in u.items()
        }
    }


def write_dict(d, fn):
    """Write dict to disk
    """
    if not type(fn) == str:
        fn = str(fn)
    with open(fn, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=4)


def flatten(items, keep_dict=False):
    """Yield items from any nested iterable; see Reference.
    # https://stackoverflow.com/a/40857703/4028896

    keep_dict: do not flatten dicts
    """
    if items is None:
        return
    if keep_dict and isinstance(items, Mapping):
        yield items
    else:
        for x in items:
            if (
                isinstance(x, Iterable)
                and not isinstance(x, (str, bytes))
                and (not keep_dict or not isinstance(x, Mapping))
            ):
                for sub_x in flatten(x, keep_dict):
                    yield sub_x
            else:
                yield x
