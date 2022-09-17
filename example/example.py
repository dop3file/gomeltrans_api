import requests


from_stop = input('Введите остановку, с которой вам надо уехать: ')
to_stop = input('Введите остановку, на которую вам надо прихеать: ')

data = requests.get(f"https://gomeltrans.pythonanywhere.com/route/routes_from_stops/?from={from_stop}&to={to_stop}")
print(data.json())