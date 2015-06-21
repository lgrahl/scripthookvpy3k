"""
Primitive UI elements.
"""
import gta_native

from gta.ui import Item, Point

__all__ = ('Rectangle', 'Label')


class Rectangle(Item):
    def draw(self, offset=Point.Zero, **settings):
        # Override default settings
        settings.update(self._settings)

        # Calculate position and dimension
        x, y = self.get_coordinates(offset)
        width, height = self.get_dimension()

        # Use native functions to draw
        # TODO: Remove logging
        from gta import utils
        utils.get_logger('gta.RECTANGLE').warning(
            'x: {}, y: {}, width: {}, height: {}, color: {}',
            x, y, width, height, self.color.rgba)
        gta_native.graphics.draw_rect(x, y, width, height, *self.color.rgba)

class Label(Item):
    pass
