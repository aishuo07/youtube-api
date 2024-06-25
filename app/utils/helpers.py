from typing import Type, TypeVar, Any, Callable, Dict, cast

import dataclasses

T = TypeVar('T')


def from_dict(cls, data: Dict[str, Any]):
    if dataclasses.is_dataclass(cls):
        fieldtypes = {f.name: f.type for f in dataclasses.fields(cls)}
        return cls(**{f: from_dict(fieldtypes[f], data[f]) for f in data if f in fieldtypes})
    elif isinstance(data, (list, tuple)):
        return [from_dict(cls.__args__[0], i) for i in data]
    else:
        return data