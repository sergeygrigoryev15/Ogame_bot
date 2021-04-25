from prettytable import PrettyTable
from loguru import logger
from enum import Enum


class Color(Enum):
    RED = 'r'
    GREEN = 'g'
    YELLOW = 'y'
    BLUE = 'b'
    WHITE = 'w'


class Painter:
    @staticmethod
    def colored_text(text, color: Color) -> str:
        if not color:
            return text
        return f'<{color.value}>{text}</{color.value}>'


class LogLevel(Enum):
    DEBUG = logger.debug
    WARNING = logger.warning
    ERROR = logger.error
    INFO = logger.info


class Logger:
    @staticmethod
    def info(text):
        logger.info(text)

    @staticmethod
    def debug(text):
        logger.debug(text)

    @staticmethod
    def warning(text):
        logger.warning(text)

    @staticmethod
    def error(text):
        logger.error(text)

    @staticmethod
    def make_table(table_data, coloring=None):
        """
        Makes table to print. input data should be a list of dicts
        Coloring is a dict like {'a': lambda x:x>1} will appeal to column named 'a'
        """
        table = PrettyTable()
        table.field_names = table_data[0].keys()
        if coloring:
            for row in table_data:
                for key, value in coloring.items():
                    text = row.get(key, '-')
                    color = Color.GREEN if value(text) else Color.RED
                    row[key] = Painter.colored_text(text, color)
        for row in table_data:
            table.add_row(row.values())
        logger.opt(colors=True).info(f'\n{table}')


if __name__ == "__main__":
    data = [{'a': 12, 'b': 'asd'}, {'a': 1, 'b': 'aeufheipouhf'}]
    Logger.warning('This is warning')
    Logger.error('Error message')
    Logger.debug('Debug message')
    Logger.make_table(data, coloring={'a': lambda x: x > 3})
