import json


def load_data_from_json(transport_type: str) -> dict:
    with open(f'{transport_type}.json', encoding='utf-8') as file:
        data = json.load(file)

    return data
    

