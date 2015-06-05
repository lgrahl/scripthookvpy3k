import os

# Enable asyncio debug logging
os.environ['PYTHONASYNCIODEBUG'] = '1'

import ast
import functools
import pkgutil
import importlib
import asyncio
import threading
import atexit

import gta_native

from gta import exceptions
from gta.exceptions import *

__author__ = 'Lennart Grahl <lennart.grahl@gmail.com>'
__status__ = 'Development'
__version__ = '0.9.12'
__all__ = exceptions.__all__


def _reset_globals():
    """
    Set global attributes.
    """
    global _utils, _thread, _loop, _tasks, _names, _tick_future, _key_future
    _utils = None
    _thread = None
    _loop = None
    _tasks = []
    _names = []
    try:
        _tick_future.cancel()
        _key_future.cancel()
    except NameError:
        pass
    _tick_future = asyncio.Future()
    _key_future = asyncio.Future()


def _init(console=False):
    """
    Run startup function in another thread.

    Arguments:
        - `console`: Use console logging instead of file logging.
    """
    _reset_globals()
    global _thread

    # Start thread
    _thread = threading.Thread(target=_start, args=(console,), daemon=True)
    _thread.start()


def _start(console):
    """
    Initialise requirements and startup scripts in an event loop.

    Arguments:
        - `console`: Use console logging instead of file logging.
    """
    global _utils, _loop, _names, _tasks

    # Import utils
    # Note: This needs to be done here because the logging module binds
    #       some vars to the thread which causes exceptions when
    #       pip invokes the logger.
    from gta import utils
    _utils = utils

    # Setup logging
    _utils.setup_logging(console)
    logger = _utils.get_logger()

    # Create event loop
    _loop = asyncio.new_event_loop()
    asyncio.set_event_loop(_loop)

    # Print some debug information
    logger.info('Started')
    logger.info('Version: {}', __version__)
    logger.info('Natives Date: {}', gta_native.__version__)

    # Start scripts
    _names, _tasks = _start_scripts(_loop)
    if len(_tasks) > 0:
        try:
            _loop.run_until_complete(asyncio.wait(_tasks))
        except RuntimeError:
            bad_scripts = [(name, task) for name, task in zip(_names, _tasks)
                           if not task.done()]

            # Mark bad behaving scripts as done
            for name, task in bad_scripts:
                # Note: We log the task so scripters can see in which line their script
                # was running when cancelled
                logger.error('Script "{}" did not stop in time, Task: {}', name, task)
                # Note: At this point, the task is marked as done but callbacks will
                # not be called anymore. We are just doing this to comfort asyncio
                # to not throw any exceptions because the task wasn't marked done
                task.set_result(BadBehavingScriptError())

            # Report bad behaving scripts
            scripts = ', '.join(('"{}"'.format(name) for name, task in bad_scripts))
            logger.warning('Enforced stopping loop, caused by script(s): {}', scripts)

    logger.info('Complete')


def _tick():
    """
    Handle a game tick event.
    """
    if _loop is not None and not _loop.is_closed():
        def __tick():
            global _tick_future
            #_utils.get_logger().debug('SET RESULT ON {}', id(_tick_future))  # TODO: Remove
            _tick_future.set_result(None)
            _tick_future = asyncio.Future()
            #_utils.get_logger().debug('NEW FUTURE {}', id(_tick_future))  # TODO: Remove
        _loop.call_soon_threadsafe(__tick)


def _key(code, down, **modifiers):
    """
    Handle a key event.

    Arguments:
        - `code`: The key code represented as an integer.
        - `down`: `True` if the key is pressed, `False` if the key was just released.
        - `modifiers`: Modifier keys pressed.
    """
    if _loop is not None and not _loop.is_closed():
        logger = _utils.get_logger()
        logger.debug("Key '{}', down: {}, modifiers: {}", code, down, modifiers)

        def __key_event():
            global _key_future
            _key_future.set_result((code, down, modifiers))
            _key_future = asyncio.Future()
        _loop.call_soon_threadsafe(__key_event)


def _exit():
    """
    Schedule stopping scripts.
    """
    if _loop is not None and not _loop.is_closed():
        logger = _utils.get_logger()
        logger.debug('Scheduling script termination')

        # Schedule stop routine
        def __stop(loop):
            logger.debug('Stopping scripts')
            loop.create_task(_stop(loop))
        _loop.call_soon_threadsafe(__stop, _loop)


@atexit.register
def _join():
    """
    Try to join the event loop thread.
    """
    # Note: _utils might be none when _init wasn't called
    if _utils is None:
        return
    logger = _utils.get_logger()

    # Wait until the thread of the event loop terminates
    if _thread is not None:
        logger.debug('Joining')
        _thread.join(timeout=1.1)
        if _thread.is_alive():
            logger.error('Joining timed out, terminating ungracefully')

    # Reset globals and exit
    _reset_globals()
    logger.info('Exiting')


@asyncio.coroutine
def _stop(loop, seconds=1.0):
    """
    Stop scripts, wait for tasks to clean up or until a timeout occurs
    and stop the loop.

    Arguments:
        - `loop`: The :class:`asyncio.BaseEventLoop` that is being used.
        - `seconds`: The maximum amount of seconds to wait.
    """
    logger = _utils.get_logger()

    # Stop scripts
    _stop_scripts(_tasks)

    # Wait for scripts to clean up
    logger.debug('Waiting for scripts to stop')
    yield from asyncio.wait(_tasks, timeout=seconds)

    # Stop loop
    logger.debug('Stopping loop')
    loop.stop()


def _start_scripts(loop):
    """
    Run the main function of all scripts from the `scripts` package.

    Arguments:
        - `loop`: The :class:`asyncio.BaseEventLoop` that is going to be used.

    Return a tuple containing a list of imported script names and
    another list that maps the script names to:class:`asyncio.Task`
    instances.
    """
    logger = _utils.get_logger()
    logger.info('Starting scripts')

    # Start each script as a coroutine
    names = []
    tasks = []
    for name, script in _import_scripts():
        logger.info('Starting script "{}"', name)
        task = loop.create_task(script())
        task.add_done_callback(functools.partial(_script_done, name=name))
        names.append(name)
        tasks.append(task)
    logger.info('Scripts started')
    return names, tasks


def _stop_scripts(tasks):
    """
    Cancel scripts that are still running.

    Arguments:
        - `tasks`: A list of :class:`asyncio.Task` instances.
    """
    logger = _utils.get_logger()
    logger.info('Cancelling scripts')
    for task in tasks:
        task.cancel()
    logger.info('Scripts cancelled')


def _import_scripts():
    """
    Import all scripts from the `scripts` package and install
    dependencies.

    Return a list containing tuples of each scripts name and the
    callback to the main function of the script.
    """
    logger = _utils.get_logger()

    # Import parent package
    parent_package = 'scripts'
    importlib.import_module(parent_package, __name__)

    # Import scripts from package
    path = os.path.join(_utils.get_directory(), parent_package)
    scripts = []
    for importer, name, is_package in pkgutil.iter_modules([path]):
        try:
            try:
                # Get meta data
                metadata = _scrape_metadata(path, name, is_package)
                logger.debug('Script "{}" metadata: {}', name, metadata)
                # Get dependencies from meta data
                dependencies = metadata.get('dependencies', ())
                # Make to tuple if string
                if isinstance(dependencies, str):
                    dependencies = (dependencies,)
            except AttributeError:
                dependencies = ()

            try:
                # Install dependencies
                for dependency in dependencies:
                    _utils.install_dependency(dependency)
            except TypeError as exc:
                raise ScriptError() from exc

            try:
                # Import script
                logger.debug('Importing script "{}"', name)
                module = importlib.import_module('.' + name, parent_package)
                main = getattr(module, 'main')
                # Make sure that main is a co-routine
                if not asyncio.iscoroutinefunction(main):
                    raise ScriptError(
                        'Main function of script "{}" is not a co-routine'.format(name))
                scripts.append((name, main))
            except (ImportError, AttributeError) as exc:
                raise ImportScriptError(name) from exc
        except ScriptError as exc:
            # Note: We are not re-raising here because script errors should not
            #       affect other scripts that run fine
            logger.exception(exc)

    # Return scripts list
    return scripts


def _scrape_metadata(path, name, is_package):
    # Update path
    if is_package:
        path = os.path.join(path, name, '__init__.py')
    else:
        path = os.path.join(path, name + '.py')

    # Open script path
    metadata = {}
    with open(path) as file:
        for line in file:
            # Find metadata strings
            if line.startswith('__'):
                try:
                    # Store key and value
                    key, value = line.split('=', maxsplit=1)
                    key = key.strip().strip('__')
                    # Note: Literal eval tries to retrieve a value, assignments,
                    #       calls, etc. are not possible
                    value = ast.literal_eval(value.strip())
                    metadata[key] = value
                except (ValueError, SyntaxError) as exc:
                    raise ImportScriptError(name) from exc
    return metadata


def _script_done(task, name=None):
    """
    Log the result or the exception of a script that returned.

    Arguments:
        - `task`: The :class:`asyncio.Future` instance of the script.
        - `name`: The name of the script.
    """
    logger = _utils.get_logger()

    try:
        try:
            # Check for exception or result
            script_exc = task.exception()
            if script_exc is not None:
                raise ScriptExecutionError(name) from script_exc
            else:
                result = task.result()
                result = ' with result "{}"'.format(result) if result is not None else ''
                logger.info('Script "{}" returned{}', name, result)
        except asyncio.CancelledError:
            logger.info('Script "{}" cancelled', name)
        except asyncio.InvalidStateError as exc:
            raise ScriptError('Script "{}" done callback called but script is not done'
                              ''.format(name)) from exc
    except ScriptError as exc:
        logger.exception(exc)


@asyncio.coroutine
def _tick_event(count=1):
    """
    Wait for one or more game ticks.

    .. warning:: Instead of using this function in your script, you
                 should write a coroutine and create a pull request on
                 GitHub.

    Arguments:
        - `count`: The amount of game ticks to wait for.
    """
    ticks = 0
    while count > ticks:
        #_utils.get_logger().debug('WAITING FOR {}', id(_tick_future))  # TODO: Remove
        yield from asyncio.shield(_tick_future)
        ticks += 1
        #_utils.get_logger().debug('WAITING DONE {}', ticks)  # TODO: Remove
    return


@asyncio.coroutine
def _key_event(code=None, modifiers=None):
    if modifiers is None:
        modifiers = {}
