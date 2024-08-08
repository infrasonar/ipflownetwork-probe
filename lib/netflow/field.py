from .field_type import FieldType


class Field:
    def __init__(self, field_id: int, length: int):
        # self._fmt
        self.id = field_id
        self.length = length
        try:
            self.name = FieldType(field_id).name.lower()
        except Exception:
            self.name = None
