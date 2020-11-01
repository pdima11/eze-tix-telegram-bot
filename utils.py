from datetime import datetime
from models import RequestStatus, Request


def str_to_datetime(date, time):
    return datetime.strptime(' '.join([str(date.date()), time]), '%Y-%m-%d %H:%M')


def build_request(user_id, args):
    transporter = args[0]
    departure, arrival = args[1].split('-')
    date = datetime.strptime(args[2], '%Y-%m-%d')
    from_time, to_time = args[3].split('-')

    return Request(
        request_id=None,
        user_id=user_id,
        transporter=transporter,
        departure=departure,
        arrival=arrival,
        required_date=date,
        from_time=str_to_datetime(date, from_time),
        to_time=str_to_datetime(date, to_time),
        status=RequestStatus.created,
        created_at=datetime.now(),
        closed_at=None
    )

