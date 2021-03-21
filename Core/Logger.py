from prettytable import PrettyTable
from loguru import logger


class Color:
    RED = "\033[1;31;48m"  # RED
    GREEN = "\033[1;32;48m"  # GREEN
    YELLOW = "\033[1;33;48m"  # Yellow
    BLUE = "\033[1;34;48m"  # Blue

    NONE = "\033[0m"


class Painter:

    @staticmethod
    def colored_text(text, color):
        if not color:
            return text
        return f'{color} {text} {Color.NONE}'


class LogLevel:
    DEBUG = None
    WARNING = Color.YELLOW
    ERROR = Color.RED

    ALL = [DEBUG, WARNING, ERROR]


class Logger:

    def __init__(self, print_buffer=None):
        self.print_buffer = print_buffer if print_buffer else []

    def add(self, element, log_level=LogLevel.DEBUG):
        self.print_buffer.append((element, log_level))

    def print_all(self):
        for element in self.print_buffer:
            self.log(*element)
        self.print_buffer = []

    def log(self, text, log_level=LogLevel.DEBUG):
        logger.log(Painter.colored_text(text, log_level))

    def debug(self, text):
        self.log(text)

    def warning(self, text):
        self.log(text, log_level=LogLevel.WARNING)

    def error(self, text):
        self.log(text, log_level=LogLevel.ERROR)

    def make_table(self, data, coloring=None):
        """
        Makes table to print. input data should be a list of dicts
        Coloring is a dict like {'a': lambda x:x>1} will appeal to column named 'a'
        """
        table = PrettyTable()
        table.field_names = data[0].keys()
        if coloring:
            for row in data:
                for key, value in coloring.iteritems():
                    text = row.get(key)
                    color = Color.GREEN if value(text) else Color.RED
                    row[key] = Painter.colored_text(text, color)
        for row in data:
            table.add_row(row.values())
        return table


if __name__ == "__main__":
    data = [{'a': 12, 'b': 'asd'}, {'a': 1, 'b': 'aeufheipouhf'}]
    logger = Logger()
    logger.warning('This is warning')
    logger.error('Error message')
    logger.log(logger.make_table(data, coloring={'a': lambda x: x > 3}))
