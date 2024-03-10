import os
import logging
from logging.handlers import RotatingFileHandler


def logg(path):
    _logger = logging.getLogger(path)
    _logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(path, backupCount=10, maxBytes=1000000)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    _logger.addHandler(handler)
    return _logger


def logger(path):

    def __logger(old_function):
        # почему так не работает? path по циклу меняется, но логи пишутся в один файл log_1.log
        # logging.basicConfig(level=logging.INFO, filename=path, filemode='w',
        #                    format="%(asctime)s %(levelname)s %(message)s")
        def new_function(*args, **kwargs):
            _logger = logg(path)
            _logger.info(old_function.__name__)
            result = old_function(*args, **kwargs)
            _logger.info(f"This function running with {args} {kwargs}")
            _logger.info(f"Result is {result}")
            _logger.handlers.clear()
            return result

        return new_function

    return __logger


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def hello_world():
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_2()
