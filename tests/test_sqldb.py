import unittest
import unittest.mock as mock

import sqldb


class SqldbTest(unittest.TestCase):
    @mock.patch('os.environ', {
        'DATABASE_URI': 'postgresql://user:pass@localhost/db'
    })
    def test_get_database_uri(self):
        self.assertEqual(sqldb.get_database_uri(),
                         'postgresql://user:pass@localhost/db')
        self.assertEqual(sqldb.get_database_uri(),
                         'postgresql://user:pass@localhost/db')

    @mock.patch('os.environ', {
        'SQL_USER': 'user',
        'SQL_PASSWORD': 'pass',
        'SQL_DATABASE': 'db'
    })
    def test_get_database_uri_no_database_uri_env(self):
        self.assertEqual(sqldb.get_database_uri(),
                         'postgresql://user:pass@localhost/db')

    @mock.patch('os.environ', {})
    def test_get_database_uri_fail(self):
        self.assertIsNone(sqldb.get_database_uri())
