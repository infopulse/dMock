from tortoise.contrib import test
from tortoise.contrib.test import initializer, finalizer
from dmock.middleware.json_transform import flatten_json, sort_flat_json, get_wild_cards, is_subset, clear_wild_keys


class TestMock(test.TestCase):
    def setUp(self):
        initializer(['dmock.models.models'], db_url='sqlite://:memory:')

    def tearDown(self):
        finalizer()

    def test_no_flat(self):
        data = {'a': 1, 'b': 'c', 'd': True, 'e': None}
        self.assertEqual(flatten_json(data), data)

    def test_list(self):
        data = [1, 2, 3, 4, 'aaa', True, None]
        self.assertEqual(flatten_json(data), {'0': 1, '1': 2, '2': 3, '3': 4, '4': 'aaa', '5': True, '6': None})

    def test_list_dict(self):
        data = [1, 2, 3, 4, {'a': 'b', 'c': 'd'}]
        self.assertEqual(flatten_json(data), {'0': 1, '1': 2, '2': 3, '3': 4, '4.a': 'b', '4.c': 'd'})

    def test_nested_1(self):
        data = {'a': 1, 'b': 'c', 'd': {'e': 'f', 'g': 'h'}}
        self.assertEqual(flatten_json(data), {'a': 1, 'b': 'c', 'd.e': 'f', 'd.g': 'h'})

    def test_nested_2(self):
        data = {'a': 'b',
                'c': 'd',
                'e': [1, 2, 3],
                'f':
                    {'g': 'h',
                     'i':
                         {'j': 'k',
                          'l':
                              {'m': 'n'}}}}
        expected = {'a': 'b',
                    'c': 'd',
                    'e.0': 1, 'e.1': 2, 'e.2': 3,
                    'f.g': 'h',
                    'f.i.j': 'k',
                    'f.i.l.m': 'n'}
        self.assertEqual(flatten_json(data), expected)

    def test_wild_cards(self):
        data1 = {'a': 1, 'b': 'c', 'd': 'e'}
        self.assertEqual(get_wild_cards(data1), [])

        data2 = {'a': 1, 'b': '*', 'd': 3}
        self.assertEqual(get_wild_cards(data2), ['b'])

        data3 = {'a': 1, 'b': '*', 'd': 3, 'x': '*'}
        self.assertEqual(get_wild_cards(data3), ['b', 'x'])

    def test_is_subset(self):
        big = {'a': 1, 'b': 2, 'c': 3}
        small1 = {'a': 1, 'b': 2}
        small2 = {'a': 1, 'b': 2, 'c': 3}
        small3 = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        self.assertTrue(is_subset(small1, big))
        self.assertTrue(is_subset(small2, big))

        self.assertFalse(is_subset(small3, big))

    def test_is_not_subset(self):
        big = {'a': 1, 'b': 2, 'c': 3}
        small1 = {'a': 1, 'b': 2, 'd': 4}
        small2 = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        self.assertFalse(is_subset(small1, big))
        self.assertFalse(is_subset(small2, big))

    def test_clear_wild_keys(self):
        data = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        wild_keys = ['b', 'd']
        self.assertEqual(clear_wild_keys(data, wild_keys), {'a': 1, 'c': 3})

    def test_clear_wild_keys_empty(self):
        data = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        wild_keys = []
        self.assertEqual(clear_wild_keys(data, wild_keys), data)
        wild_keys = ['xxx', 'yyy']
        self.assertEqual(clear_wild_keys(data, wild_keys), data)