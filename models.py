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
