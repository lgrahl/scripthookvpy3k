import asyncio

import gta_native

from gta.events import player

__all__ = ('in_vehicle',)


@asyncio.coroutine
def in_vehicle(ped=None, precision=10):
    """
    Wait until a ped is in a vehicle.

    Arguments:
        - `ped`: The id of a ped, defaults to player.
        - `precision`: The amount of game ticks to wait for.

    Return the vehicle the ped is using.
    """
    while True:
        # Wait for the player if no ped has been set
        if ped is None:
            ped = yield from player.exists(precision)
        # Check if the ped is in a vehicle
        if gta_native.ped.is_ped_in_any_vehicle(ped, 0):
            vehicle = gta_native.ped.get_vehicle_ped_is_using(ped)
            return vehicle
