# Script Hook V Py3k
This is an ASI plugin for Grand Theft Auto V that wraps around the C++ ScriptHook by Alexander Blade. It allows running scripts written in Python 3 in game by using the included [GTA module](/python/gta.py).

## Download
Coming soon.

## Installation
1. Install the [Script Hook V](http://www.dev-c.com/gtav/scripthookv/)
2. Install [Python 3.4.3 for Windows x64](https://www.python.org/ftp/python/3.4.3/python-3.4.3.amd64.msi).
3. Extract the contents of the archive into your GTA V folder.

## Scripting
See [/example](/example) to get started.

Copy your ``.py`` script file into ``scripts`` in your GTA V folder.

Press F12 in game to reload all scripts.

## Building
If you want to build the ASI plugin yourself, you'll need Visual Studio 2013 and the [Script Hook V SDK](http://www.dev-c.com/gtav/scripthookv/) which has to be extracted into [/sdk](/sdk) after downloading.

Install **Python 3 for AMD64/EM64T/x64**. Using the x86 version will not work!

Open the project file and build the solution in *Release* configuration.
