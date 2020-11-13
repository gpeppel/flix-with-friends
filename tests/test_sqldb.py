import unittest
import unittest.mock as mock

import sqldb


class SqldbTest(unittest.TestCase):
	@mock.patch('os.environ', {
		'SQL_USER': 'user',
		'SQL_PASSWORD': 'pass',
		'SQL_DATABASE': 'db'
	})
	def test_get_database_uri(self):
		self.assertEqual(sqldb.getDatabaseUri(), 'postgresql://user:pass@localhost/db')
