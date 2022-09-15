from django.conf import settings
from django.http import JsonResponse

from .utils import load_data_from_json
from .misc import _get_route_from_stops


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

    data = _get_route_from_stops(stop_from, stop_to)
    response = {'response': data, 'status_code': 200}

    return JsonResponse(response, safe=True)
    