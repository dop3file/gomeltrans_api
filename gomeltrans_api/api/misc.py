from .utils import load_data_from_json


def _get_route_with_stops(stop_from: str, stop_to: str, is_weekday: bool) -> dict:
    all_transports_info: dict[dict] = {
        'bus': load_data_from_json('bus'), 
        'trolleybus': load_data_from_json('trolleybus')
    }

    suitable_routes = []

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
    print(suitable_routes)