import asyncio

import gta.utils
import gta_native

__author__ = 'Lennart Grahl <lennart.grahl@gmail.com>'
__status__ = 'Production'
__version__ = '1.0.0'


@asyncio.coroutine
def main():
    """
    Increase the wanted level by one.
    """
    logger = gta.utils.get_logger('gta.wanted')
    logger.debug('Hello')
    player = gta_native.player.player_id()
    logger.debug('Player: {}', player)
    wanted_level = gta_native.player.get_player_wanted_level(player) + 1
    logger.debug('New wanted level: {}', wanted_level)
    gta_native.player.set_player_wanted_level(player, wanted_level, False)
    gta_native.player.set_player_wanted_level_now(player, False)
