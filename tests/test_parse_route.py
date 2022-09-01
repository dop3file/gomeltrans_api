import json


def load_data_from_file(file_name):
    with open(file_name, encoding='utf-8') as json_file:
        data = json.load(json_file)

    return data


def test_stop_times():
    assert load_data_from_file('../json_data_async.json')['15']['stops']['to']['Вокзал']['week'][0] == '5:55', 'First stop time test'
    
def test_stop_times():
    assert load_data_from_file('../json_data_async.json')['20']['stops']['to']['БелГУТ']['weekend'][5] == '9:58', 'Second stop time test'

def test_stop_times():
    assert load_data_from_file('../json_data_async.json')['43']['stops']['to']['Большевик']['week'][14] == '14:49', 'Third stop time test'


    