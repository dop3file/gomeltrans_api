import json


def load_data_from_file():
    with open('../parser/json_data_async.json') as json_file:
        data = json.load(json_file)
    return data


def test_parse_stop_times():
    assert load_data_from_file()['15']['to']['Вокзал'][0] == '5:55'