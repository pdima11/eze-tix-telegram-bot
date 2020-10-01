from datetime import datetime
from models import TicketRequest


def str_to_datetime(date, time):
    return datetime.strptime(' '.join([str(date.date()), time]), '%Y-%m-%d %H:%M')


def build_request(request_id, args):
    transporter = args[0]
    departure, arrival = args[1].split('-')
    date = datetime.strptime(args[2], '%Y-%m-%d')
    from_time, to_time = args[3].split('-')

    return TicketRequest(
        request_id,
        transporter,
        departure,
        arrival,
        date,
        str_to_datetime(date, from_time),
        str_to_datetime(date, to_time)
    )

