import os
import pkgutil
import importlib
import atexit
import asyncio

from gta import utils

__all__ = ('ScriptException', 'ImportScriptException', 'get_logger')


class ScriptException(Exception):
    pass


class ImportScriptException(ScriptException):
    def __str__(self):
        return 'Could not import script: {}'.format(*self.args)


def _init():
    # Setup logging
    utils.setup_logging()

    # Print some debug information
    logger = utils.get_logger()
    logger.debug('Started')

    # Start scripts
    _start_scripts()


def _import_scripts():
    logger = utils.get_logger()

    # Import parent package
    parent_package = 'scripts'
    importlib.import_module(parent_package, __name__)

    # Import scripts from package
    directory = os.path.join(os.getcwd(), parent_package)
    for importer, package_name, _ in pkgutil.iter_modules([directory]):
        try:
            try:
                module = importlib.import_module('.' + package_name, parent_package)
                main = getattr(module, 'main')
                yield (package_name, main)
            except (ImportError, AttributeError) as exc:
                raise ImportScriptException(package_name) from exc
        except ScriptException as exc:
            logger.exception(exc)


def _start_scripts():
    logger = utils.get_logger()
    logger.debug('Starting scripts')

    # Start each script as a coroutine
    loop = asyncio.get_event_loop()
    tasks = []
    for name, script in _import_scripts():
        logger.debug('Starting script: {}', name)
        task = loop.create_task(script())
        tasks.append(task)
    logger.debug('Scripts started')
    if len(tasks) > 0:
        loop.run_until_complete(asyncio.wait(tasks))
    loop.close()


def _stop_scripts():
    logger = utils.get_logger()
    logger.debug('Stopping scripts')
    # TODO: Close event loop (cancel tasks)

@atexit.register
def _exit():
    logger = utils.get_logger()
    _stop_scripts()
    logger.debug('Exiting')
