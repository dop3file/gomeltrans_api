from datetime import datetime

from .utils import load_data_from_json


def is_weekday():
    return datetime.now().weekday() < 5


def _sort_nearest_routes(routes: list[dict], stop_from: str):
    '''
    Функция сортирует маршруты по времени прибытия к остановке с которой надо уехать
    routes - массив маршрутов
    stop_from - остановка, с которой надо уехать
    '''
    stop_times = []
    for index, route in enumerate(routes):
        stop_times.extend([[index, datetime.strptime(stop_time, '%H:%M')] for stop_time in load_data_from_json(route['transport_type'])[route['number']]['stops'][route['side']][stop_from]['week' if is_weekday() else 'weekend']])
    #print(stop_times)
    dt = datetime(1900, 1, 1, datetime.now().hour, datetime.now().minute)
    nearest_stop = sorted(stop_times[len(stop_times) // 2::], key = lambda d: d[1] - dt)
    return {
        "route_info": routes[nearest_stop[0][0]],
        "stop_time": nearest_stop[0][1].strftime("%H:%M")
    }


def _get_route_from_stops(stop_from: str, stop_to: str) -> dict:
    '''
    Функция возвращает все маршруты включающие stop_from и stop_to
    stop_from - остановка, с которой надо уехать
    stop_to - остановка, на которую надо прибыть
    '''
    all_transports_info: dict[dict] = {
        'bus': load_data_from_json('bus'), 
        'trolleybus': load_data_from_json('trolleybus')
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