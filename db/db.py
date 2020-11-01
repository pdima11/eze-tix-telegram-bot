import psycopg2
import psycopg2.extras
from config import DATABASE_URL


class UserSQL(object):
    save = '''
        INSERT INTO users (user_id, username, first_name, last_name, is_bot, language_code, last_visit) 
        VALUES (%(user_id)s, %(username)s, %(first_name)s, %(last_name)s, %(is_bot)s, %(language_code)s, %(visit_datetime)s)
        ON CONFLICT (user_id) DO UPDATE 
        SET username = excluded.username, 
            first_name = excluded.first_name,
            last_name = excluded.last_name,
            language_code = excluded.language_code,
            last_visit = excluded.last_visit;
    '''


class RequestSQL(object):
    create = '''
        INSERT INTO requests (user_id, transporter, departure, arrival, required_date, from_time, to_time, status, created_at) 
        VALUES (%(user_id)s, %(transporter)s, %(departure)s, %(arrival)s, %(required_date)s, %(from_time)s, %(to_time)s, %(status)s, %(created_at)s)
        RETURNING request_id
    '''

    update_status_by_id = '''
        UPDATE requests
        SET status = %s
        WHERE request_id = %s
    '''


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