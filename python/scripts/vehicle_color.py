import asyncio
import random

import gta.utils
import gta_native

__author__ = 'Lennart Grahl <lennart.grahl@gmail.com>'
__status__ = 'Production'
__version__ = '1.0.0'


@asyncio.coroutine
def main():
    """
    Applies a different vehicle colour on each 100th game tick.
    """
    logger = gta.utils.get_logger('gta.vehicle_color')

    while True:
        logger.debug('Waiting for 100 ticks')
        yield from gta.tick(count=100)
        player_ped = gta_native.player.player_ped_id()
        player_exists = lambda: gta_native.entity.does_entity_exist(player_ped)
        player_in_vehicle = lambda: gta_native.ped.is_ped_in_any_vehicle(player_ped, 0)

        # Make sure the player exists and is in a vehicle
        if player_exists() and player_in_vehicle():
            vehicle = gta_native.ped.get_vehicle_ped_is_using(player_ped)
            # Generate colour
            color = [random.randint(0, 255) for _ in range(3)]
            # Apply colour
            logger.debug('Changing vehicle color to: {}', color)
            gta_native.vehicle.set_vehicle_custom_primary_colour(vehicle, *color)
        else:
            logger.debug('No player existing or not in a vehicle')
