import asyncio
import random

import gta.utils
import gta_native
import aiohttp

__author__ = 'Lennart Grahl <lennart.grahl@gmail.com>'
__status__ = 'Development'
__version__ = '0.9.1'
__dependencies__ = ('aiohttp>=0.15.3',)


@asyncio.coroutine
def main():
    """
    Applies the current weather from Los Angeles in game.
    """
    url = 'http://api.openweathermap.org/data/2.5/weather?id=3882428'
    logger = gta.utils.get_logger('gta.weather-time')
    map_weather_id = {
        'WIND': (900, 905, 771),
        'EXTRASUNNY': (904,),
        'CLEAR': (800, 801),
        'CLOUDS': (802, 803, 804),
        'SMOG': (711, 751, 761, 762),
        'FOGGY': (701, 721, 731, 741),
        'OVERCAST': (),
        'RAIN': (500, 501, 502, 503, 504, 511, 520, 521, 522, 531, 311, 312, 313, 314,
                 321),
        'THUNDER': (200, 201, 202, 210, 211, 212, 221, 230, 231, 232, 900, 901, 902, 781),
        'CLEARING': (300, 301, 302, 310),
        'NEUTRAL': (),
        'SNOW': (903, 906, 601, 611, 612, 615, 622),
        'BLIZZARD': (602, 621),
        'SNOWLIGHT': (600, 616, 620),
        'XMAS': ()
    }

    while True:
        # Get weather in Los Angeles
        logger.debug('Requesting {}', url)
        response = yield from aiohttp.request('get', url)
        try:
            json = yield from response.json()
        except ValueError:
            logger.warning('Parsing response failed')
            continue
        logger.debug('Response: {}', json)

        # Calculate weather type
        weather_types = {}
        try:
            # Map OpenWeatherMap IDs to GTA weather types and apply a rating
            for weather in json['weather']:
                id_ = weather['id']
                for weather_type, ids in map_weather_id.items():
                    if id_ in ids:
                        weather_types.setdefault(weather_type, 0)
                        weather_types[weather_type] += 1

            # Get the weather types with the highest rating
            highest = max(weather_types.values())
            weather_types = [weather_type for weather_type, count in weather_types.items()
                             if count == highest]

            # When there are multiple weather types with the same rating, choose randomly
            if len(weather_types) > 1:
                logger.debug('Randomly choosing from: {}', weather_types)
                weather = random.choice(weather_types)
            else:
                weather, *_ = weather_types
        except (ValueError, KeyError):
            logger.warning('Could not parse weather data')
            yield from asyncio.sleep(10.0)
            continue

        # Apply weather type in GTA
        logger.info('Setting weather to: {}', weather)
        gta_native.gameplay.set_weather_type_now_persist(weather)
        gta_native.gameplay.clear_weather_type_persist()

        # TODO: Set wind
        # gta_native.gameplay.set_wind(1.0)
        # gta_native.gameplay.set_wind_speed(11.99)
        # gta_native.gameplay.set_wind_direction(gta_native.entity.get_entity_heading(gta_native.player.player_ped_id()))

        # TODO: Set time

        # Wait for a minute
        yield from asyncio.sleep(60.0)
