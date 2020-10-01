import requests
from bs4 import BeautifulSoup
import json
from models import TicketResponse
from utils import str_to_datetime


class Transporter9911(object):
    def __init__(self, config):
        self.config = config

    def __get_free_seats_by_time(self, seats, times, request):
        result = []
        for seat, time in zip(seats, times):
            seat_datetime = str_to_datetime(request.date, time.text)
            seats_count = int(seat.text)
            if seats_count > 0 and request.from_time <= seat_datetime <= request.to_time:
                result.append(TicketResponse(seat_datetime, seats_count))

        return result

    def __build_request_data(self, request):
        return {
            'type': 'load_list_order',
            'select_in': self.config['locations'][request.departure],
            'select_out': self.config['locations'][request.arrival],
            'date': request.date.strftime(self.config['date_format']),
            'strGET': ''
        }

    def find_ticket(self, request):
        data = self.__build_request_data(request)

        response = requests.request("POST", self.config['url'], data=data, files=[])

        parsed_html = BeautifulSoup(json.loads(response.text)["alert"], 'html.parser')
        seats = parsed_html.find_all('span', attrs={'class': 'lol_driver_space_num'})
        times = parsed_html.find_all('div', attrs={'class': 'lol_time'})

        tickets = self.__get_free_seats_by_time(seats, times, request)
        return tickets
