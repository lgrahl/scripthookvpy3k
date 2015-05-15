import asyncio

import gta.utils

# The following metadata will not be processed but is recommended
# Author name and E-Mail
__author__ = 'Full Name <email@example.com>'
# Status of the script: Use one of 'Prototype', 'Development', 'Production'
__status__ = 'Development'

# The following metadata will be parsed and should always be provided
# Version number: This should always be a string and formatted in the x.x.x notation
__version__ = '0.0.1'
# A list of dependencies in the requirement specifiers format
# See: https://pip.pypa.io/en/latest/reference/pip_install.html#requirement-specifiers
__dependencies__ = ('aiohttp>=0.15.3',)


@asyncio.coroutine
def main():
    """
    Does absolutely nothing but show you how to provide metadata.
    """
    logger = gta.utils.get_logger('gta.metadata')
    logger.debug('Hello from the metadata example')
