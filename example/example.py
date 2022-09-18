from datetime import datetime
import requests


from_stop = input('Введите остановку, с которой вам надо уехать: ')
to_stop = input('Введите остановку, на которую вам надо прихеать: ')

avialable_transports = requests.get(f"https://gomeltrans.pythonanywhere.com/route/routes_from_stops/?from={from_stop}&to={to_stop}").json()['response']
nearest_transport = requests.get(f"https://gomeltrans.pythonanywhere.com/route/nearest_route/?from={from_stop}&to={to_stop}").json()['response']

for transport in avialable_transports:
    type_transport = 'Автобус' if transport['transport_type'] == 'bus' else 'Тролейбус'
    print(f'{transport["number"]} {type_transport}')

print('-' * 10)
print('Самый ближайший транспорт: ')
type_transport = 'Автобус' if nearest_transport["route_info"]["transport_type"] == 'bus' else 'Тролейбус'
transport_stop_time = datetime.strptime(nearest_transport["stop_time"], '%H:%M')
print(transport_stop_time)
time_delta: list = str(transport_stop_time - datetime.now()).split(" ")[-1].split(":")[0:2]

print(f'{nearest_transport["route_info"]["number"]} {type_transport} - осталось {time_delta[0] + " часа " if time_delta[0] != "0" else ""}{time_delta[1]} минуты')  