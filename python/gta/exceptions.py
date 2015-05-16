__all__ = ('ScriptError', 'ImportScriptError', 'InstallDependencyError',
           'DependencyBlacklistedError', 'ScriptExecutionError', 'BadBehavingScriptError')


class ScriptError(Exception):
    """
    A general script exception all other exceptions are derived from.
    """
    pass


class ImportScriptError(ScriptError):
    """
    A script could not be imported.

    Arguments:
        - `name`: The name of the script.
    """
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'Could not import script "{}"'.format(self.name)


class InstallDependencyError(ScriptError):
    """
    A script dependency could not be installed.

    Arguments:
        - `dependency`: The dependency name.
    """
    def __init__(self, dependency):
        self.dependency = dependency

    def __str__(self):
        return 'Dependency needs to be installed manually via pip "{}"'.format(
            self.dependency)


class DependencyBlacklistedError(ScriptError):
    """
    A script dependency is blacklisted and cannot be installed.

    Arguments:
        - `dependency`: The dependency name.
    """
    def __init__(self, dependency):
        self.dependency = dependency

    def __str__(self):
        return 'Could not install dependency "{}"'.format(self.dependency)


class ScriptExecutionError(ScriptError):
    """
    An uncaught exception was raised in a script.

    Arguments:
        - `name`: The name of the script.
    """
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'Script "{}" returned with an exception'.format(self.name)


class BadBehavingScriptError(ScriptError):
    """
    A script did not stop in time after it has been cancelled.

    Arguments:
        - `name`: The name of the script.
    """
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'Script "{}" did not stop in time'.format(self.name)
