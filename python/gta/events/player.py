import asyncio

import gta_native

from gta import events

__all__ = ('exists',)


@asyncio.coroutine
def exists(precision=10):
    """
    Wait until the player exists.

    Arguments:
        - `precision`: The amount of game ticks to wait for.

    Return the player ped.
    """
    while True:
        # Check if the player ped exists
        player_ped = gta_native.player.player_ped_id()
        if gta_native.entity.does_entity_exist(player_ped):
            return player_ped
        yield from events.tick(precision)
