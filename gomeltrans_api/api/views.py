from django.conf import settings
from django.http import JsonResponse

from .utils import load_data_from_json
from .misc import _get_route_from_stops, _sort_nearest_routes

from datetime import datetime
import functools


def get_route(request, type_transport: str, number: str):
    response = {'response': None, 'status_code': 200}

    if type_transport not in settings.TRANSPORT_TYPES:
        response['status_code'] = 404
        return JsonResponse(response)
    try:
        response['response'] = load_data_from_json(type_transport)[number]
    except KeyError:
        response['status_code'] = 404

    return JsonResponse(response, safe=True)


def get_all_name_routes(request, type_transport: str):
    data = list(load_data_from_json(type_transport).keys())
    response = {'response': data, 'status_code': 200}

    return JsonResponse(response, safe=True)


def get_route_from_stops(request):
    stop_from = request.GET.get('from', '')
    stop_to = request.GET.get('to', '')

    routes = functools.reduce(lambda a, b: a + b, [_get_route_from_stops(transport_type, stop_from, stop_to) for transport_type in settings.TRANSPORT_TYPES])

    response = {'response': routes, 'status_code': 200 if routes else 404}

    return JsonResponse(response, safe=True)


def get_nearest_route(reqeust):
    stop_from = reqeust.GET.get('from', '')
    stop_to = reqeust.GET.get('to', '')

    get_nearest_route = lambda type_transport: _sort_nearest_routes(_get_route_from_stops(type_transport, stop_from, stop_to), stop_from)

    bus_nearest_route = get_nearest_route('bus')
    trolleybus_nearest_route = get_nearest_route('trolleybus')
    

    nearest_route = bus_nearest_route if bus_nearest_route and trolleybus_nearest_route and datetime.strptime(bus_nearest_route.get('stop_time'), "%H:%M") < datetime.strptime(trolleybus_nearest_route.get('stop_time'), "%H:%M") else trolleybus_nearest_route if trolleybus_nearest_route else bus_nearest_route if bus_nearest_route else None

    response = {'response': nearest_route, 'status_code': 200 if nearest_route else 404}

    return JsonResponse(response, safe=True)
    