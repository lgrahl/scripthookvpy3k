import ast
import os
import pkgutil
import importlib
import asyncio
import threading

from gta import exceptions
from gta.exceptions import *

__author__ = 'Lennart Grahl <lennart.grahl@gmail.com>'
__status__ = 'Development'
__version__ = '0.9.0'
__all__ = exceptions.__all__

# Global objects
_utils = None
_thread = None
_loop = None
_tasks = []
_names = []


def _init(console=False):
    """
    Initialise requirements and startup scripts in an event loop.

    Arguments:
        - `console`: Use console logging instead of file logging.
    """
    global _thread, _loop, _utils, _names, _tasks

    # Store current thread
    _thread = threading.current_thread()

    # Import utils
    # Note: This needs to be done here because the logging module binds
    #       some vars to the thread which causes exceptions when
    #       pip invokes the logger.
    from gta import utils
    _utils = utils

    # Store event loop
    _loop = asyncio.get_event_loop()

    # Setup logging
    _utils.setup_logging(console)

    # Print some debug information
    logger = _utils.get_logger()
    logger.info('Started')

    # Start scripts
    _names, _tasks = _start_scripts(_loop)
    if len(_tasks) > 0:
        try:
            _loop.run_until_complete(asyncio.wait(_tasks))
        except RuntimeError:
            # Report bad behaving scripts
            scripts = ', '.join(('"{}"'.format(name) for name, task in zip(_names, _tasks)
                                 if not task.done()))
            logger.warning('Enforced stopping loop, caused by script(s): {}', scripts)

    logger.info('Complete')


def _exit():
    """
    Schedule stopping scripts and exit.
    """
    logger = _utils.get_logger()

    # Schedule stopping scripts
    if _loop is not None and not _loop.is_closed():
        def __stop(loop):
            loop.create_task(_stop(loop))
        _loop.call_soon_threadsafe(__stop, _loop)

    # Wait until the thread of the event loop terminates
    if _thread is not None:
        logger.debug('Joining')
        _thread.join()

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
    path = os.path.join(os.getcwd(), parent_package)
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
