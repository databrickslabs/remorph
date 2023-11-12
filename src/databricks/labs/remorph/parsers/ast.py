import dataclasses
import functools


def node(cls):
    cls = functools.partial(dataclasses.dataclass, slots=True, match_args=True, frozen=True, repr=False)(cls)
    fields = dataclasses.fields(cls)

    def __repr__(self):
        values = []
        for field in fields:
            v = getattr(self, field.name)
            if v is None:
                continue
            if field.type == bool and not v:
                continue
            values.append(f'{field.name}={v}')
        return f'{cls.__name__}({", ".join(values)})'

    __repr__.__qualname__ = f"{cls.__qualname__}.__repr__"
    setattr(cls, '__repr__', __repr__)

    return cls
