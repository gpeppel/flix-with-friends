import re

import psycopg2
import psycopg2.extras


class SqlDb:
    def __init__(self):
        self.connection = None

    def connect(self, dsn):
        self.connection = psycopg2.connect(dsn)

    def disconnect(self):
        self.connection.close()
        self.connection = None

    def cursor(self):
        return self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def commit(self):
        self.connection.commit()

    def is_connected(self):
        return self.connection is not None

    @staticmethod
    def uri_to_dsn(uri):
        match = re.match(
            r'postgresql://(?:(?P<user>[^:]+)(?::(?P<password>[^@]+))?@)?(?P<host>[^/:]+)(?::(?P<port>[0-9]+))?(?:/(?P<dbname>[^?]+))?(?:\?(?P<query>.*))?',
            uri
        )
        if match is None:
            return None

        groups = match.groupdict()

        def sanitize(val):
            if len(val) == 0:
                return "''"

            val = val.replace('\\', '\\\\')
            val = val.replace("'", "\\'")

            if ' ' in val:
                return "'%s'" % val
            return val

        dsn = ""
        for key, val in groups.items():
            if val is None:
                continue
            dsn += " %s=%s" % (key, sanitize(val))
        dsn = dsn[1:]

        return dsn
