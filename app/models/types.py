from sqlalchemy.types import TypeDecorator, Integer


class IntEnumType(TypeDecorator):
    """
    Map Python IntEnum <-> Integer column.
    Stores enum.value (int) in DB, returns enum instance when loaded.
    """
    impl = Integer
    cache_ok = True  # SQLAlchemy 1.4+ optimization hint

    def __init__(self, enum_class, **kwargs):
        super().__init__(**kwargs)
        self._enum_class = enum_class

    def process_bind_param(self, value, dialect):
        # value may be IntEnum, int, or None
        if value is None:
            return None
        if isinstance(value, self._enum_class):
            return int(value.value)
        # allow passing raw integer
        return int(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return self._enum_class(int(value))

    def copy(self, **kw):
        return IntEnumType(self._enum_class)
