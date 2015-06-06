# Script Hook V Py3k
This is an ASI plugin for Grand Theft Auto V that allows you to execute Python 3 scripts
in game by using the Script Hook V from Alexander Blade.

## Features
* All [native functions](http://www.dev-c.com/nativedb/) accessible
* Scripts run as lightweight asynchronous tasks
* High level [requirement functions](/python/gta/requires) can be chained and waited for
* All the [fancy Python packages out there](https://warehouse.python.org) can be used
  and...
* Dependencies will be installed automatically

## Download
Prebuilt binaries can be found on the [releases](../../releases)
page.

## Installation
1. Install the [Script Hook V](http://www.dev-c.com/gtav/scripthookv/)
2. Install [Python 3.4.3 for Windows x64](https://www.python.org/ftp/python/3.4.3/python-3.4.3.amd64.msi)
3. Copy the contents of the downloaded archive into your GTA V game folder

## Writing Scripts
To get started on writing scripts, head over to [this wiki page](../../wiki/Writing-Scripts).

## Contributing
All contributions are warmly welcomed. Below are a few hints to the entry points of the
code and a link to our to do list.

### Entry Points
* ``Py3kWrapperStart`` in [wrapper.cpp](/cpp/src/wrapper.cpp) is the entry point for the
  C++ part of the plugin
* ``_init`` in [the gta module](/python/gta/__init__.py) is the entry point for the
  Python part of the plugin

### Todo
See [TODO.md](/TODO.md).

## Building
If you want to build the ASI plugin yourself, you'll need:

1. Visual Studio 2013
2. The [Script Hook V SDK](http://www.dev-c.com/gtav/scripthookv/) which has to be
   extracted into [/sdk](/sdk) after downloading
3. [SWIG](http://sourceforge.net/projects/swig/files/swigwin/) Version >= 3.0.5 which has
   to be extracted into [/swig](/swig) after downloading
4. **Python 3 for AMD64/EM64T/x64**. Using the x86 version will not work!
5. Open the project file and build the solution in *Release* configuration
