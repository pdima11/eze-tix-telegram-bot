import psycopg2
import psycopg2.extras
from config import DATABASE_URL


class DB(object):
    _conn = None

    @classmethod
    def __get_conn(cls):
        if cls._conn is None:
            cls._conn = psycopg2.connect(DATABASE_URL)

        return cls._conn

    @classmethod
    def execute(cls, sql, params=None, *, autocommit=True):
        with cls.__get_conn().cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            try:
                cur.execute(sql, params)
                if autocommit:
                    cls.__get_conn().commit()

                if cur.description is not None:
                    return list(cur)
            except psycopg2.DatabaseError as e:
                if autocommit:
                    cls.__get_conn().rollback()
                raise e