from datetime import datetime
from enum import Enum


class TicketRequest(object):
    def __init__(self, req_id, transporter, departure, arrival, date, from_time, to_time):
        self.id = req_id
        self.transporter = transporter
        self.departure = departure
        self.arrival = arrival
        self.date = date
        self.from_time = from_time
        self.to_time = to_time


class TicketResponse(object):
    def __init__(self, datetime, seats):
        self.datetime = datetime
        self.seats = seats

    def __repr__(self):
        return f'Datetime: {str(self.datetime)}, Free seats - {self.seats}'


class User(object):
    def __init__(self,
                 user_id,
                 username,
                 first_name,
                 last_name,
                 is_bot,
                 language_code,
                 visit_datetime):
        self.id = user_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.is_bot = is_bot
        self.language_code = language_code
        self.visit_datetime = visit_datetime

    @classmethod
    def from_dict(cls, data):
        return cls(
            user_id=data['id'],
            username='@' + data['username'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            is_bot=data['is_bot'],
            language_code=data['language_code'],
            visit_datetime=datetime.now()
        )

    def asdict(self):
        return {
            'user_id': self.id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_bot': self.is_bot,
            'language_code': self.language_code,
            'visit_datetime': str(self.visit_datetime)
        }


class RequestStatus(Enum):
    created = 'CREATED'
    in_progress = 'IN_PROGRESS'
    done = 'DONE'


class Request(object):
    def __init__(self,
                 request_id,
                 user_id,
                 transporter,
                 departure,
                 arrival,
                 required_date,
                 from_time,
                 to_time,
                 status,
                 created_at,
                 closed_at):
        self.id = request_id
        self.user_id = user_id
        self.transporter = transporter
        self.departure = departure
        self.arrival = arrival
        self.required_date = required_date
        self.from_time = from_time
        self.to_time = to_time
        self.status = status
        self.created_at = created_at
        self.closed_at = closed_at

    def asdict(self):
        return {
            'request_id': self.id,
            'user_id': self.user_id,
            'transporter': self.transporter,
            'departure': self.departure,
            'arrival': self.arrival,
            'required_date': str(self.required_date),
            'from_time': str(self.from_time.time()),
            'to_time': str(self.to_time.time()),
            'status': self.status.value,
            'created_at': str(self.created_at),
            'closed_at': str(self.closed_at),
        }
