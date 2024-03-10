from main_1 import logger
import os


class FlatIterator:

    def __init__(self, list_of_list):
        self.list_of_lists = [i for lst in list_of_list for i in lst]

    def __iter__(self):
        self.items = iter(self.list_of_lists)
        return self

    def __next__(self):
        item = next(self.items)
        return item


if os.path.exists('log_4.log'):
    os.remove('log_4.log')


@logger('log_4.log')
def test_1():

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):
        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]


if __name__ == '__main__':
    test_1()
