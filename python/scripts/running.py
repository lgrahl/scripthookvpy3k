import asyncio

import gta.utils

__author__ = 'Lennart Grahl <lennart.grahl@gmail.com>'
__status__ = 'Production'
__version__ = '1.0.0'


@asyncio.coroutine
def main():
    """
    Yields every second and shouts at the logger.
    """
    logger = gta.utils.get_logger('gta.running')
    counter = 0
    while True:
        logger.debug("{} times and counting!", counter)
        yield from asyncio.sleep(1.0)
        counter += 1
