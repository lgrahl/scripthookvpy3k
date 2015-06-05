import asyncio

import gta
import gta_native

from gta import Key, utils
from gta.events import key
from gta.requires import player

__author__ = 'Lennart Grahl <lennart.grahl@gmail.com>'
__status__ = 'Production'
__version__ = '2.0.0'


@asyncio.coroutine
def main():
    """
    Increase the wanted level when `+` is pressed.
    Decrease the wanted level when `-` is pressed.
    Double increase or decrease when `Shift` is pressed as well.
    """
    logger = utils.get_logger('gta.wanted')

    while True:
        # Wait until '+' or '-' has been pressed
        code, _, modifiers = yield from key(codes={Key.ADD, Key.SUBTRACT})
        number = 2 if modifiers['shift'] else 1

        try:
            # Get player id and wanted level
            player_id = player.get_id()
            wanted_level = gta_native.player.get_player_wanted_level(player_id)
            logger.debug('Wanted level is {}', wanted_level)

            # Increase or decrease wanted level
            if code == Key.ADD and wanted_level < 5:
                wanted_level = min(wanted_level + number, 5)
                logger.debug('Increasing wanted level to {}', wanted_level)
            elif code == Key.SUBTRACT and wanted_level > 0:
                wanted_level = max(wanted_level - number, 0)
                logger.debug('Decreasing wanted level to {}', wanted_level)

            # Apply wanted level
            gta_native.player.set_player_wanted_level(player_id, wanted_level, False)
            gta_native.player.set_player_wanted_level_now(player_id, False)
        except gta.RequirementError as exc:
            logger.debug(exc)
