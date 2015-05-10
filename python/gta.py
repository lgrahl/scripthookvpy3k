import logging
import os
import sys
import atexit

import gta_native

class Message:
    """
    A wrapper class that applies the new formatting style on a message
    and it's arguments.

    It's safe to throw any object in here that has a __str__ method
    (e.g. an exception).

    ..note:: Using keywords in the formatter will not work.

    Arguments:
        - `fmt`: A formatter string or an object that has a __str__
          method.
        - `args`: Arguments that will be passed to the formatter.
    """

    def __init__(self, fmt, args):
        """Create a message instance with formatter and arguments."""
        self._fmt = fmt
        self._args = args

    def __str__(self):
        """
        Return a formatted string using curly brackets.

        The __str__ method will be called if :attr:`_fmt` is not a
        string.
        """
        if isinstance(self._fmt, str):
            return self._fmt.format(*self._args)
        else:
            return self._fmt.__str__()
            
class CurlyBracketFormattingAdapter(logging.LoggerAdapter):
    """
    Logging style adapter that is able to use the new curly bracket
    formatting style.

    Arguments:
        - `logger`: Instance of :class:`logging.Logger`.
        - `extra`: Optional dict-like object that will be passed to
          every log message and can be used for formatting.
    """
    def __init__(self, logger, extra=None):
        super().__init__(logger, extra or {})

    def log(self, level, msg, *args, **kwargs):
        """
        Pass a log message. Shouldn't be called directly. Use level
        methods instead (e.g. info, warning, etc.).
        """
        if self.isEnabledFor(level):
            msg, kwargs = self.process(msg, kwargs)
            # noinspection PyProtectedMember
            self.logger._log(level, Message(msg, args), (), **kwargs)

def _init():
    # Setup logging
    _setup_logging()

    # Print some debug information
    logger = get_logger()
    logger.debug('Path: {}', sys.path)
    
    # Start scripts
    _start_scripts()

def _setup_logging():
    # Setup formatter and handler
    formatter = logging.Formatter(
        fmt='{asctime} {name:<22} {levelname:<18} {message}',
        datefmt='%Y-%m-%d %H-%M:%S',
        style='{'
    )
    handler = logging.FileHandler('scripthookvpy3k.log')
    handler.setFormatter(formatter)
    
    # Setup gta logger
    logger = logging.getLogger('gta')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    
def _start_scripts():
    logger = get_logger()
    logger.debug('Starting scripts')
    
    # TODO: Start each script
    try:
        player = gta_native.PLAYER_ID()
        player_ped = gta_native.PLAYER_PED_ID()
        logger.debug('PLAYER: {}', player)
        wanted_level = gta_native.GET_PLAYER_WANTED_LEVEL(player) + 1
        gta_native.SET_PLAYER_WANTED_LEVEL(player, wanted_level, False)
        gta_native.SET_PLAYER_WANTED_LEVEL_NOW(player, False)
    except Exception as exc:
        logger.exception(exc)


def _stop_scripts():
    logger = get_logger()
    logger.debug('Stopping scripts')

@atexit.register
def _exit():
    logger = get_logger()
    _stop_scripts()
    logger.debug('Exiting')

def get_logger(name='gta'):
    return CurlyBracketFormattingAdapter(logging.getLogger(name))
