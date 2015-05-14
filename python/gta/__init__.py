import ast
import os
import pkgutil
import importlib
import atexit
import asyncio

from gta import utils, exceptions
from gta.exceptions import *

__author__ = 'Lennart Grahl <lennart.grahl@gmail.com>'
__status__ = 'Development'
__version__ = '0.9.0'
__all__ = exceptions.__all__


def _init(console=False):
    """
    Initialise requirements and startup scripts.

    Arguments:
        - `console`: Use console logging instead of file logging.
    """
    # Setup logging
    utils.setup_logging(console)

    # Print some debug information
    logger = utils.get_logger()
    logger.info('Started')

    # Start scripts
    _start_scripts()


def _start_scripts():
    """
    Run the main function of all scripts from the `scripts` package.
    """
    logger = utils.get_logger()
    logger.info('Starting scripts')

    # Start each script as a coroutine
    loop = asyncio.get_event_loop()
    tasks = []
    for name, script in _import_scripts():
        logger.info('Starting script "{}"', name)
        task = loop.create_task(script())
        tasks.append(task)
    logger.info('Scripts started')
    if len(tasks) > 0:
        loop.run_until_complete(asyncio.wait(tasks))
    loop.close()


def _stop_scripts():
    """
    Cancel scripts that are still running.
    """
    logger = utils.get_logger()
    logger.info('Stopping scripts')
    # TODO: Cancel tasks


@atexit.register
def _exit():
    """
    Stop running scripts and clean up before exiting.
    """
    logger = utils.get_logger()
    _stop_scripts()
    logger.info('Exiting')


def _import_scripts():
    """
    Import all scripts from the `scripts` package and install
    dependencies.

    Return a list containing tuples of each scripts name and the
    callback to the main function of the script.
    """
    logger = utils.get_logger()

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
                    utils.install_dependency(dependency)
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
