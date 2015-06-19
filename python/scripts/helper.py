import asyncio

import gta.utils

__author__ = 'Lennart Grahl <lennart.grahl@gmail.com>'
__status__ = 'Development'
__version__ = '0.0.1'


@asyncio.coroutine
def main():
    """
    Various tools that should help scripters doing their work.
    """
    logger = gta.utils.get_logger('gta.helper')
