# Script Hook V Py3k
This is an ASI plugin for Grand Theft Auto V that wraps around the C++ ScriptHook by
Alexander Blade. It allows running scripts written in Python 3 in game by using the
included [GTA module](/python/gta).

## Features

* All native functions from ScriptHook accessible
* Dependencies will be installed automatically
* Scripts run as lightweight asynchronous tasks
* High level [requirement functions](/python/requires) can be chained and waited for

## Download
Coming soon.

## Installation
1. Install the [Script Hook V](http://www.dev-c.com/gtav/scripthookv/)
2. Install [Python 3.4.3 for Windows x64](https://www.python.org/ftp/python/3.4.3/python-3.4.3.amd64.msi)
3. Extract the contents of the downloaded archive into your GTA V folder

## Writing Scripts
Please, read [Develop with asyncio](https://docs.python.org/3/library/asyncio-dev.htm)
before you start.

See [/python/scripts](/python/scripts) for a list of examples.

If you want to mock-test your script, you can run [simulate.py](/tools/simulate.py) in
the [/python](/python) directory.

You can (and should) provide metadata in your script. See
[metadata.py](/python/scripts/metadata.py) for details.

To run the script in GTA V, copy your ``.py`` script file into ``python/scripts`` in your
GTA V folder.

Press Ctrl+F12 in game to reload all scripts or Ctrl+Del to just stop them.

## Building
If you want to build the ASI plugin yourself, you'll need:
* Visual Studio 2013
* The [Script Hook V SDK](http://www.dev-c.com/gtav/scripthookv/) which has to be
  extracted into [/sdk](/sdk) after downloading
* [SWIG](http://sourceforge.net/projects/swig/files/swigwin/) Version >= 3.0.5 which has
  to be extracted into [/swig](/swig) after downloading
* **Python 3 for AMD64/EM64T/x64**. Using the x86 version will not work!

Open the project file and build the solution in *Release* configuration.
