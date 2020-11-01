import requests
from models import TicketResponse
from utils import str_to_datetime


class Transporter618(object):
    def __init__(self, config):
        self.config = config

    def __get_free_seats_by_time(self, seats, times, request):
        result = []
        for seats_count, time in zip(seats, times):
            seat_datetime = str_to_datetime(request.required_date, time)
            if seats_count > 0 and request.from_time <= seat_datetime <= request.to_time:
                result.append(TicketResponse(seat_datetime, seats_count))

        return result

    def __build_request_data(self, request):
        return {
            'departure_is_waypoint': '0',
            'arrival_is_waypoint': '0',
            'id_departure_station': self.config['locations'][request.departure],
            'id_arrival_station': self.config['locations'][request.arrival],
            'date': request.required_date.strftime(self.config['date_format']),
        }

    def find_ticket(self, request):
        data = self.__build_request_data(request)

        response = requests.request("POST", self.config['url'], params=data)
        json = response.json()

        seats = [item['count'] for item in json]
        times = [item['time'].split('-')[0].strip() for item in json]

        tickets = self.__get_free_seats_by_time(seats, times, request)
        return tickets
