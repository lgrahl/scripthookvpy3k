import asyncio
import random

import gta_native

from gta import utils
from gta.events import ped

__author__ = 'Lennart Grahl <lennart.grahl@gmail.com>'
__status__ = 'Production'
__version__ = '1.0.0'


@asyncio.coroutine
def main():
    """
    Applies a different vehicle colour on each 100th game tick.
    """
    logger = utils.get_logger('gta.vehicle_color')

    while True:
        # Wait until the player is in a vehicle with a precision of 100 ticks
        vehicle = yield from ped.in_vehicle(precision=100)
        # Generate colour
        color = [random.randint(0, 255) for _ in range(3)]
        # Apply colour
        logger.debug('Changing vehicle color to: {}', color)
        gta_native.vehicle.set_vehicle_custom_primary_colour(vehicle, *color)
