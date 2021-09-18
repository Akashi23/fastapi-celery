from typing import List
from time import sleep
import requests
from datetime import datetime
from datetime import timedelta
from redis import Redis
from ..config import REDIS_STORE
import json

redis_instance = Redis.from_url(REDIS_STORE)

headers = {
    'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
    'x-rapidapi-key': "cb86834b20msh871eb3f15edc4e0p1a0848jsnc87eaf789ba8"
    }


details_air = [
    {
        "country": "KZ",
        "currency": "KZT",
        "origin": "ALA",
        "destination": "NQZ",
    },
    {
        "country": "KZ",
        "currency": "KZT",
        "origin": "ALA",
        "destination": "VKO",
    },
    {
        "country": "KZ",
        "currency": "KZT",
        "origin": "ALA",
        "destination": "CIT",
    },
    {
        "country": "KZ",
        "currency": "KZT",
        "origin": "NQZ",
        "destination": "VKO",
    },
    {
        "country": "KZ",
        "currency": "KZT",
        "origin": "NQZ",
        "destination": "LED",
    },
]


def reverse_and_add_routes(details: List[dict]) -> List[dict]:
    details_all: List[dict] = []
    for detail in details:
        reverse_detail = detail.copy()
        reverse_detail['destination'] = detail['origin']
        reverse_detail['origin'] = detail['destination']
        details_all.append(detail)
        details_all.append(reverse_detail)

    return details_all 
    

def months_day_table() -> List[str]:
    """Table or List with year-month-day string for iterating request"""
    def increment_day(day) -> datetime:
        now = datetime.now()
        return now + timedelta(days=day)

    day_table = [increment_day(x).strftime("%Y-%m-%d") for x in range(31)]
    return day_table


def define_url(detail: dict, date: str) -> str:
    """Creating URL for every request"""
    try:
        url: str = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com"+\
            "/apiservices/browsedates/v1.0"+\
            f"/{detail['country']}/{detail['currency']}/ru-{detail['country']}"+\
            f"/{detail['origin']}-sky/{detail['destination']}-sky/{date}"
    except ValueError as e:
        return e
    return url


def request_to_api_by_details(detail: dict) -> dict:
    """Request to api with Route Details"""
    month_table: List[str] = months_day_table()
    all_response: List[dict] = []
    index = 0 # for counting request and printing console

    for day in month_table:
        sleep(1)

        url = define_url(detail, day)

        data_with_additional_info = requests.request("GET", url, headers=headers).json() # ALL Data in response

        data_without: dict
        if not data_with_additional_info["Quotes"]:
            data_without = { 'date': day }

        for i in data_with_additional_info['Quotes']:
            data_without = { 'date': day, 'minPrice': i['MinPrice']}

        all_response.append(data_without)
        index += 1

        print(f"Ready {detail['origin']}-{detail['destination']} {index} {data_without}")
    return { f"{detail['origin']}-{detail['destination']}": all_response}


def get_calendar_of_all_route():
    """For receiving all Routes calendar with min price"""
    air_routes = reverse_and_add_routes(details_air)
    calendar_with_routes: dict = {}
    for route in air_routes:
        calendar_with_routes.update(request_to_api_by_details(route))
    return calendar_with_routes


def save_all_route_to_redis():
    """Save all route via redis.set such as key 'ALA-NQZ': [Array]"""
    air_routes = reverse_and_add_routes(details_air)
    for route in air_routes:
        calendar: dict = request_to_api_by_details(route)
        key: str = list(calendar.keys())[0]
        redis_instance.set(key, json.dumps(calendar[key]))

    return "Saved!"
