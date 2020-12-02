import unittest

import utils


OBJECT = 'object'
KEY = 'key'
VALUE = 'value'

GETVAL = [
    {
        OBJECT: {
            'test': 123
        },
        KEY: 'test',
        VALUE: 123
    },
    {
        OBJECT: {
            'parent': {
                'child': 'hello'
            }
        },
        KEY: 'parent.child',
        VALUE: 'hello'
    },
    {
        OBJECT: {
            'test': 123
        },
        KEY: 'noexist',
        VALUE: None
    }
]


class UtilsTest(unittest.TestCase):
    def test_getval(self):
        for entry in GETVAL:
            self.assertEqual(utils.getval(entry[OBJECT], entry[KEY]), entry[VALUE])
