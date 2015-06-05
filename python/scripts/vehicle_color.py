import asyncio
import random

import gta_native

from gta import utils
from gta.events import wait
from gta.requires import player

__author__ = 'Lennart Grahl <lennart.grahl@gmail.com>'
__status__ = 'Production'
__version__ = '1.1.1'


@asyncio.coroutine
def main():
    """
    Applies a different vehicle colour every second.
    """
    logger = utils.get_logger('gta.vehicle_color')

    while True:
        # Wait until the player is in a vehicle with a precision of 100 ticks
        vehicle = yield from wait(player.get_vehicle, precision=100)
        # Generate colour
        color = [random.randint(0, 255) for _ in range(3)]
        # Apply colour
        logger.debug('Changing vehicle color to: {}', color)
        gta_native.vehicle.set_vehicle_custom_primary_colour(vehicle, *color)
        # Because the coroutine usually returns immediately, we want to
        # wait a second, so the script isn't spamming colours every tick
        yield from asyncio.sleep(1.0)
