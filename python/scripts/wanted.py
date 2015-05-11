import asyncio

import gta.utils
import gta_native


@asyncio.coroutine
def main():
    logger = gta.utils.get_logger('gta.wanted')
    player = gta_native.PLAYER_ID()
    logger.debug('PLAYER: {}', player)
    wanted_level = gta_native.GET_PLAYER_WANTED_LEVEL(player) + 1
    gta_native.SET_PLAYER_WANTED_LEVEL(player, wanted_level, False)
    gta_native.SET_PLAYER_WANTED_LEVEL_NOW(player, False)
