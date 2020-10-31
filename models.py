from datetime import datetime


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