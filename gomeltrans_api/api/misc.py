from datetime import datetime, timedelta
from time import time

from .utils import load_data_from_json


TIME_NOW = lambda: datetime.now()


def is_weekday():
    return TIME_NOW().weekday() < 5

def _sort_nearest_routes(routes: list[dict], stop_from: str):
    '''
    Функция сортирует маршруты по времени прибытия к остановке с которой надо уехать
    routes - массив маршрутов
    stop_from - остановка, с которой надо уехать
    '''
    try:
        stop_times = []
        #print(routes)
        for index, route in enumerate(routes):
            stop_times.extend([[index, datetime(year=TIME_NOW().year, month=TIME_NOW().month, day=TIME_NOW().day, hour=int(stop_time.split(':')[0]), minute=int(stop_time.split(':')[1]))] for stop_time in load_data_from_json(route['transport_type'])[route['number']]['stops'][route['side']][stop_from]['week' if is_weekday() else 'weekend']])

        nearest_route = [stop_time for stop_time in stop_times if (stop_time[1] - TIME_NOW()).total_seconds() > 0]

        return {
                "route_info": routes[nearest_route[0][0]],
                "stop_time": nearest_route[0][1].strftime("%H:%M"),
                "local_time": TIME_NOW()
                }


    except IndexError:
        return None


def _get_route_from_stops(transport_type: str, stop_from: str, stop_to: str) -> dict:
    '''
    Функция возвращает все маршруты включающие stop_from и stop_to
    stop_from - остановка, с которой надо уехать
    stop_to - остановка, на которую надо прибыть
    '''
    all_transports_info: dict[dict] = {
        transport_type: load_data_from_json(transport_type),
    }

    suitable_routes: list[dict] = []

    for transport_type, transport in all_transports_info.items():
        add_route = lambda side: suitable_routes.append({
                    'transport_type': transport_type,
                    'number': number,
                    'side': side
                })
        for number, info in transport.items():
            get_stop_index = lambda global_side, side_index: list(info['stops'][global_side].keys()).index(side_index)
            if all([info['stops']['to'].get(stop) for stop in (stop_from, stop_to)]) and get_stop_index('to', stop_to) > get_stop_index('to', stop_from):
                add_route('to')
            elif all([info['stops']['back'].get(stop) for stop in (stop_from, stop_to)]) and get_stop_index('back', stop_to) > get_stop_index('back', stop_from):
                add_route('back')
                
    return suitable_routes