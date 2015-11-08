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

        text_scale = 0.4

        line_width = 350.0
        line_height = 15.0
        line_top = 18.0
        line_left = 0.0
        text_left = 5.0

        line_width_scaled = line_width / 1280
        line_top_scaled = line_top / 720
        text_left_scaled = text_left / 1280
        line_height_scaled = line_height / 720

        line_left_scaled = line_left / 1280

        # Use native functions to draw
        logger.warning('x: {}, y: {}, width: {}, height: {}, color: {}',
               x, y, width, height, self.color.rgba)
        logger.warning('gta_native.graphics.get_screen_resolution()')
        gta_native.graphics.get_screen_resolution()
        logger.info('Screen resolution: {}', gta_native.graphics.get_screen_resolution())
        logger.warning('gta_native.ui.set_text_font(Font.chalet_london)')
        gta_native.ui.set_text_font(Font.chalet_london)
        logger.warning('gta_native.ui.set_text_scale(0.0, 0.35)')
        gta_native.ui.set_text_scale(0.0, text_scale)
        logger.warning('gta_native.ui.set_text_colour(*Color.White.rgba)')
        gta_native.ui.set_text_colour(*Color.White.rgba)
        logger.warning('gta_native.ui.set_text_centre(True)')
        gta_native.ui.set_text_centre(False)
        logger.warning('gta_native.ui.set_text_dropshadow(0, 0, 0, 0, 0)')
        gta_native.ui.set_text_dropshadow(0, 0, 0, 0, 0)
        logger.warning('gta_native.ui.set_text_edge(0, 0, 0, 0, 0)')
        gta_native.ui.set_text_edge(0, 0, 0, 0, 0)
        logger.warning('gta_native.ui._SET_TEXT_ENTRY(\'STRING\')')
        gta_native.ui._SET_TEXT_ENTRY('STRING')
        logger.warning('gta_native.ui._ADD_TEXT_COMPONENT_STRING(\'TEST\')')
        gta_native.ui._ADD_TEXT_COMPONENT_STRING('TEST')
        logger.warning('gta_native.ui._DRAW_TEXT(text_left_scaled, no_idea_1)')
        no_idea_1 = line_top_scaled + 0.00278 + line_height_scaled - 0.005
        logger.info('text_left_scaled={}, no_idea_1={}', text_left_scaled, no_idea_1)
        gta_native.ui._DRAW_TEXT(text_left_scaled, no_idea_1)
        no_idea_2 = gta_native.ui._0xDB88A37483346780(text_scale, 0)
        logger.info('line_left_scaled={}, line_top_scaled + 0.00278={}, line_width_scaled={}, no_idea_2 + line_height_scaled*2.0 + 0.005={}, *self.color.rgba={}',
                    line_left_scaled, line_top_scaled + 0.00278, line_width_scaled, no_idea_2 + line_height_scaled*2.0 + 0.005, *self.color.rgba)
        gta_native.graphics.draw_rect(
            line_left_scaled,
            line_top_scaled + 0.00278,
            line_width_scaled,
            no_idea_2 + line_height_scaled*2.0 + 0.005,
            *self.color.rgba
        )
        # gta_native.graphics.draw_rect(x, y, width, height, *self.color.rgba)

class Label(Item):
    pass
