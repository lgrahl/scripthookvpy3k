"""
Primitive UI elements.
"""
import gta_native

from gta import Font
from gta.ui import Item, Point, Color

__all__ = ('Rectangle', 'Label')


class Rectangle(Item):
    def draw(self, offset=Point.Zero, **settings):
        # TODO: Remove logging
        from gta import utils
        logger = utils.get_logger('gta.RECTANGLE')

        # Override default settings
        settings.update(self._settings)

        # Calculate position and dimension
        x, y = self.get_coordinates(offset)
        width, height = self.get_dimension()

        # Use native functions to draw
        logger.warning('gta_native.graphics.get_screen_resolution()')
        gta_native.graphics.get_screen_resolution()
        logger.info('Screen resolution: {}', gta_native.graphics.get_screen_resolution())
        logger.warning('gta_native.ui.set_text_font(Font.chalet_london)')
        gta_native.ui.set_text_font(Font.chalet_london)
        logger.warning('gta_native.ui.set_text_scale(0.0, 0.35)')
        gta_native.ui.set_text_scale(0.0, 0.35)
        logger.warning('gta_native.ui.set_text_colour(*Color.White.rgba)')
        gta_native.ui.set_text_colour(*Color.White.rgba)
        logger.warning('gta_native.ui.set_text_centre(True)')
        gta_native.ui.set_text_centre(True)
        logger.warning('gta_native.ui.set_text_dropshadow(0, 0, 0, 0, 0)')
        gta_native.ui.set_text_dropshadow(0, 0, 0, 0, 0)
        logger.warning('gta_native.ui.set_text_edge(0, 0, 0, 0, 0)')
        gta_native.ui.set_text_edge(0, 0, 0, 0, 0)
        logger.warning('gta_native.ui._SET_TEXT_ENTRY(\'STRING\')')
        gta_native.ui._SET_TEXT_ENTRY('STRING')
        logger.warning('gta_native.ui._ADD_TEXT_COMPONENT_STRING(\'TEST\')')
        gta_native.ui._ADD_TEXT_COMPONENT_STRING('TEST')
        logger.warning('gta_native.ui._DRAW_TEXT(x, y)')
        gta_native.ui._DRAW_TEXT(x, y)
        logger.warning('gta_native.ui._ADD_TEXT_COMPONENT_STRING(\'TEST\')')
        gta_native.ui._ADD_TEXT_COMPONENT_STRING('TEST')
        logger.warning('x: {}, y: {}, width: {}, height: {}, color: {}',
                       x, y, width, height, self.color.rgba)
        gta_native.graphics.draw_rect(x, y, width, height, *self.color.rgba)

class Label(Item):
    pass
