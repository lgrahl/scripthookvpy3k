import asyncio

import gta.utils
import gta_native

__author__ = 'Mathias Lechtermann <matzel1992@gmail.com>'
__status__ = 'Production'
__version__ = '0.0.1'


#Globals
_activeLineIndex = 0


def draw_rect(_A0, _A1, _A2, _A3, _A4, _A5, _A6, _A7):
	"""
	Draws a rectangle.
	"""
	gta_native.graphics.draw_rect((_A0 + (_A2 * 0.5)), (_A1 + (_A3 * 0.5)), _A2, _A3, _A4, _A5, _A6, _A7)



def draw_menu_line(caption, lineWidth, lineHeight, lineTop, lineLeft, textLeft, isactive, istitle, rescaleText=True):
	"""
	Draws a menu line.
	
	Arguments:
		-`caption`:
		-`lineWidth`:
		-`lineHeight`:
		-`lineTop`:
		-`lineLeft`:
		-`textLeft`:
		-`isactive`:
		-`istitle`:
		-`rescaleText`:
	"""
	#Default values
	global _text_col, _rect_col, _text_scale, _font
	_text_col = [255,255,255,255]
	_rect_col = [70,95,95,255]
	_text_scale = 0.35
	_font = 0
	
	#Correcting values for active line
	if(isactive):
		_text_col[0] = 0
		_text_col[1] = 0
		_text_col[2] = 0
		
		_rect_col[0] = 218
		_rect_col[1] = 242
		_rect_col[2] = 216
		
		if(rescaleText):
			_text_scale = 0.40
	
	if(istitle):
		_rect_col[0] = 0
		_rect_col[1] = 0
		_rect_col[2] = 0
		
		if(rescaleText):
			_text_scale = 0.50
			
		_font = 1
	
	global _screenW, _screenH
	gta_native.graphics.get_screen_resolution(_screenW,_screenH)
	
	textLeft+=lineLeft
	
	global _lineWidthScaled, _lineTopScaled, _lineHeightScaled, _lineLeftScaled, _textLeftScaled
	_lineWidthScaled = lineWidth/_screenW
	_lineTopScaled = lineTop/_screenH
	_lineHeightScaled = lineHeight/_screenH
	_lineLeftScaled = lineLeft/_screenW
	_textLeftScaled = textLeft/_screenW
	
	#Text upper part
	gta_native.ui.set_text_font(_font)
	gta_native.ui.set_text_scale(0.0, _text_scale)
	gta_native.ui.set_text_colour(_text_col[0], _text_col[1], _text_col[2], _text_col[3])
	gta_native.ui.set_text_center(0)
	gta_native.ui.set_text_dropshadow(0, 0, 0, 0, 0)
	gta_native.ui.set_text_edge(0, 0, 0, 0, 0)
	gta_native.ui._SET_TEXT_ENTRY("STRING")
	gta_native.ui._ADD_TEXT_COMPONENT_STRING(caption)
	gta_native.ui._DRAW_TEXT(_textLeftScaled, (((_lineTopScaled + 0.00278) + _lineHeightScaled) - 0.005))
	
	#Text lower part
	gta_native.ui.set_text_font(_font)
	gta_native.ui.set_text_scale(0.0, text_scale);
	gta_native.ui.set_text_colour(text_col[0], text_col[1], text_col[2], text_col[3]);
	ta_native.ui.set_text_center(0);
	gta_native.ui.set_text_dropshadow(0, 0, 0, 0, 0);
	gta_native.ui.set_text_edge(0, 0, 0, 0, 0);
	gta_native.ui._0x521FB041D93DD0E4("STRING");
	gta_native.ui._ADD_TEXT_COMPONENT_STRING(caption);
	global _num25 = gta_native.ui._0x9040DFB09BE75706(_textLeftScaled, (((_lineTopScaled + 0.00278) + _lineHeightScaled) - 0.005))
	
	#Rect
	draw_rect(_lineLeftScaled, _lineTopScaled+0.00278, _lineWidthScaled, ((((num25)* gta_native.ui._0xDB88A37483346780(_text_scale, 0)) + (_lineHeightScaled * 2.0)) + 0.005),_rect_col[0], _rect_col[1], _rect_col[2], rect_col[3]))
	
	

def main_menu():
	"""
	Loads the menu items and their logic.
	"""
	global _lineWidth, _lines, _caption, _waitTime
	_lineWidth = 250.0
	_waitTime = 150
	_caption = "Test Menu 0.1"
	_lines = ["Test1","Test2"]
	
	while(True):
		global _index = 0
	
		draw_menu_line(_caption, _lineWidth, 15.0, 18.0, 0.0, 5.0, False, True)
		for _line in _lines:
			if(_index != _activeLineIndex):
				draw_menu_line(_line, _lineWidth, 9.0, 60.0 + _index * 36.0, 0.0, 9.0, False, False)
			else:
				draw_menu_line(_line, _lineWidth+1.0, 11.0, 56.0,_activeLineIndex *36.0, 0.0, 7.0, True, False)
		_index++


	
@asyncio.coroutine
def main():
    """
    Displays the menu.
    """
    logger = gta.utils.get_logger('gta.menu')
    logger.debug('Hello')