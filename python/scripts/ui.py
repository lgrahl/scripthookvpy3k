import asyncio

from gta import Key, ui, utils
from gta.events import key
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
        yield from key(codes=Key.F12)
        ui.draw()

        # Modify the created UI elements
        # TODO

        counter += 1
