import asyncio

from gta import ui, utils
from gta.ui import Dimension, primitive

__author__ = 'Lennart Grahl <lennart.grahl@gmail.com>'
__status__ = 'Development'
__version__ = '0.0.1'


@asyncio.coroutine
def main():
    """
    Creates a few primitive UI elements.
    """
    logger = utils.get_logger('gta.ui')
    counter = 0

    # Create primitive UI elements
    rectangle = primitive.Rectangle(size=Dimension.Quarter)
    ui.add(rectangle)

    while True:
        yield from asyncio.sleep(1.0)

        # Modify the created UI elements
        # TODO

        counter += 1
