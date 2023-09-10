

class ValidationError(Exception):

    def __init__(self, message: str):
        self._message = message
        self._field_name_list = list()
        self._index_list = list()

    def set_index(self, index: int):
        self._index_list.insert(0, index)

    def set_field(self, field_name: str):
        if len(self._index_list) > 0:
            for index in self._index_list:
                field_name += f'[{index}]'
            self._index_list = list()

        self._field_name_list.insert(0, field_name)

    def __str__(self) -> str:
        return self._message

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}: {self._message}>'
