from collections import namedtuple


class Enum(object):

    @classmethod
    def get_by_name(cls, name):
        name = name.encode('utf-8') if isinstance(name, unicode) else name
        for el in [el for el in dir(cls) if not el.startswith('__') or not callable(getattr(cls, el))]:
            if getattr(cls, str(el)) == name:
                return el

    # TODO
    # @classmethod
    # def __getattr__(cls, item):
    #     A = namedtuple(str(item), 'name value')
    #     return A(str(item), getattr(cls, str(item)))
