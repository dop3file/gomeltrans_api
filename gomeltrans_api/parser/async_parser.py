import encodings
from inspect import Attribute
import json
import time
import asyncio
from zoneinfo import available_timezones
import aiohttp

from bs4 import BeautifulSoup


HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
}
BASE_URL = 'https://gomeltrans.net/'


async def parse_route(session, url: str) -> list:
    '''
    Функция парсит весь маршрут и его остановки в 2 стороны
    '''
    async with session.get(url=url, headers=HEADERS) as response:
        soup = BeautifulSoup(await response.text(), 'lxml')
        all_stops = soup.find_all('td', class_='stop-name')
        final_all_stops = {'to': {}, 'back': {}}

        for stop in all_stops:
            stop_link = stop.find('a', href=True)

            if stop_link:
                final_all_stops['to' if stop_link.get('href').split('/')[-2][0] == 'a' else 'back'][stop_link.text.strip()] = await parse_stop_times(session, BASE_URL + stop_link.get('href'))

        return final_all_stops


async def parse_stop_times(session, url: str) -> dict:
    '''
    Функция парсит и возвращает время остановок с ссылки url
    '''
    async with session.get(url=url, headers=HEADERS) as response:
        soup = BeautifulSoup(await response.text(), 'lxml')
        all_stop_times = soup.find_all(class_='schedule-full')

        is_week_stops = bool(soup.find('h2', class_='week-day'))
        is_weekend_stops = bool(soup.find('h2', class_='day-off'))
        
        all_stop_times_week = all_stop_times[0] if is_week_stops else None
        try:
            all_stop_times_weekend = all_stop_times[0] if is_weekend_stops and not is_week_stops else None if not is_weekend_stops else all_stop_times[1]
        except IndexError:
            all_stop_times_weekend = None

        final_stop_times = {'week': [], 'weekend': []}
        if all_stop_times_week:
            for week in all_stop_times_week.find_all(class_='sch-hour'):
                hour_week = week.find(class_='sch-h').text
                
                for minutes_week in week.find_all(class_='sch-m'):
                    final_stop_times['week'].append(f'{hour_week}:{minutes_week.text}')

        if all_stop_times_weekend:
            for weekend in all_stop_times_weekend.find_all(class_='sch-hour'):
                hour_weekend = weekend.find(class_='sch-h').text

                for minutes_weekend in weekend.find_all(class_='sch-m'):
                    final_stop_times['weekend'].append(f'{hour_weekend}:{minutes_weekend.text}')

        return final_stop_times


async def parse_all_routes(type_transport: str) -> dict:
    '''
    Функция парсит все маршруты
    type_transport - bus или trolleybus
    '''
    final_routes = {}
    
    async with aiohttp.ClientSession() as session:
        url = f'https://gomeltrans.net/routes/{type_transport}/'
        async with session.get(url=url, headers=HEADERS) as response:
            soup = BeautifulSoup(await response.text(), 'lxml')
            routes = soup.find_all(class_='routes-list')[0]

            stops = []
            all_route_numbers = []
            for route in routes.find_all('div'):
                route = route.find('a', href=True)
                route_link = route.get('href')

                async with session.get(url=BASE_URL + route_link, headers=HEADERS) as response_route:
                    soup = BeautifulSoup(await response_route.text(), 'lxml')
                    required_route_info = soup.find_all(class_='route-info-block-content big-1')
                    additional_route_info = {
                        'mode': [
                            soup.find(class_='route-info-block-content big-1 day-off'), 
                            soup.find(class_='route-info-block-content big-1 green'),
                            soup.find(class_='route-info-block-content big-1 week-day')
                        ],
                        'tariff_price': required_route_info[0].text.replace('\xa0', ''),
                        'route_length': float(required_route_info[1].text.replace('\xa0', '').replace(',', '.').replace('км','')) if len(required_route_info) < 4 else float(required_route_info[2].text.replace('\xa0', '').replace(',', '.').replace('км','')),
                        'count_stops': int(required_route_info[-1].text.replace('\xa0', ''))                        
                    }
                
                    additional_route_info['mode'] = [mode.text for mode in additional_route_info['mode'] if mode][0]
                    try:
                        additional_route_info['similar_routes'] = [element.text.split(' ')[0] for element in soup.find(class_='routes-list-little routes-list little-2').find_all('div')]
                    except AttributeError:
                        pass

                number_route: str = route.text.split(' ')[0]
                route = route.text[len(number_route) + 1:].replace('\xa0—', ' -').replace('\xa0→', ' -')

                try:
                    from_ = route.split(' - ')[0]
                    to = route.split(' - ')[1]
                except IndexError:
                    from_ = route
                    to = None

                final_routes[number_route] = {
                    'from': from_, 
                    'to': to,
                    **additional_route_info
                    }
                all_route_numbers.append(number_route)
                task = asyncio.create_task(parse_route(session, BASE_URL + route_link))
                stops.append(task)
            
            stops = await asyncio.gather(
                *stops
            )
            for index, number in enumerate(all_route_numbers):
                final_routes[number]['stops'] = stops[index]
    return final_routes

            
def write_json(result, file_name):
    with open(f'../{file_name}.json', 'w', encoding='utf-8') as outfile:
        json.dump(result, outfile, ensure_ascii=False, indent=4)


def main():
    print('Start parse')
    before = time.time()
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    all_bus_routes = asyncio.run(parse_all_routes('bus'))
    write_json(all_bus_routes, 'bus')
    all_trolleybus_routes = asyncio.run(parse_all_routes('trolleybus'))
    write_json(all_trolleybus_routes, 'trolleybus')
    print('End parse')
    print(time.time() - before)

if __name__ == '__main__':
    main()