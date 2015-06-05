"""
Commonly used events that can be waited for.

Every function returns a coroutine that has to be yielded from.
"""
import asyncio
import functools
import gta

from gta import utils

__all__ = ('tick', 'key', 'wait')


@asyncio.coroutine
def tick(count=1):
    """
    Wait for one or more game ticks.

    .. warning:: Instead of using this function in your script, you
                 should write a coroutine in the `requires` package
                 and create a pull request on GitHub.

    Arguments:
        - `count`: The amount of game ticks to wait for.
    """
    ticks = 0
    while count > ticks:
        yield from asyncio.shield(getattr(gta, '_tick_future'))
        ticks += 1
    return


@asyncio.coroutine
def key(codes=None, down=False, **modifiers):
    """
    Wait for a key to be pressed or released.

    Arguments:
        - `code`: A single :class:`Key` or a list of :class:`Key`s to
          watch for. Use ``None`` to watch all keys.
        - `down`: ``True`` returns keys when pressed, ``False`` returns
          keys when released. Use ``None`` for both cases.
        - `alt`: ``True`` requires `Alt` to be pressed as well,
          ``False`` requires `Alt` to be not pressed. Defaults to both
          cases.
        - `ctrl`: ``True`` requires `Ctrl` to be pressed as well,
          ``False`` requires `Ctrl` to be not pressed. Defaults to both
          cases.
        - `shift`: ``True`` requires `Shift` to be pressed as well,
          ``False`` requires `Shift` to be not pressed. Defaults to both
          cases.

    Return a tuple containing the actual key event values for `code`,
    `down` and `modifiers`.
    """
    if isinstance(codes, gta.Key):
        # Convert codes to tuple
        codes = (codes,)
    elif codes is not None and not isinstance(codes, set):
        # Convert iterable to set
        codes = set(codes)

    while True:
        # Unpack key event
        key_event = yield from asyncio.shield(getattr(gta, '_key_future'))
        code, down_, modifiers_ = key_event

        # Check code
        if codes is not None and code not in codes:
            continue
        # Check down
        if down_ is not None and down != down_:
            continue
        # Check modifiers
        if any((modifiers_[key_] != value for key_, value in modifiers.items())):
            continue

        # Return key event
        return key_event


@asyncio.coroutine
def wait(require_func, *args, precision=10, **kwargs):
    """
    Wait for a requirement to be fulfilled.

    Arguments:
        - `require_func`: A function from the :mod:`requires` package.
        - `precision`: The amount of game ticks to wait between checks.
        - `args`: Arguments that will be passed to the function.
        - `kwargs`: Keyword arguments that will be passed to the
          function.

    Return the value `require_func` returns when the requirement is
    fulfilled.
    """
    logger = utils.get_logger('gta.wait')

    # Create partial
    partial = functools.partial(require_func, *args, **kwargs)

    # Poll until fulfilled
    while True:
        try:
            result = partial()
            logger.debug('{} fulfilled, result: {}', partial, result)
            return result
        except gta.RequirementError as exc:
            logger.debug('{} not fulfilled, missing: {}', partial, exc.requirement)
        yield from tick(count=precision)
