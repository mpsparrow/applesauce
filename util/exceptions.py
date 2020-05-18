"""
Custom throwable exceptions
"""

class dbConnectionFail(Exception):
    """
    Raised when database connection fails
    """
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'dbConnectionFail, {0} '.format(self.message)
        else:
            return 'dbConnectionFail has been raised'

class dbCommitFail(Exception):
    """
    Raised when database commit fails
    """
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'dbCommitFail, {0} '.format(self.message)
        else:
            return 'dbCommitFail has been raised'

class dbQueryFail(Exception):
    """
    Raised when database query fails
    """
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'dbQueryFail, {0} '.format(self.message)
        else:
            return 'dbQueryFail has been raised'

class dbTableCreationFail(Exception):
    """
    Raised when database table is unable to be created
    """
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'dbTableCreationFail, {0} '.format(self.message)
        else:
            return 'dbTableCreationFail has been raised'

class configReadError(Exception):
    """
    Raised when there is an error reading a config file
    """
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'configReadError, {0} '.format(self.message)
        else:
            return 'configReadError has been raised'

class configWriteError(Exception):
    """
    Raised when there is an error writing to a config file
    """
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'configWriteError, {0} '.format(self.message)
        else:
            return 'configWriteError has been raised'

class CogNotFound(Exception):
    """
    Raised when cog is not found in db
    """
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'CogNotFound, {0} '.format(self.message)
        else:
            return 'CogNotFound has been raised'

class CogInsertFail(Exception):
    """
    Raised when cog fails to be inserted into db
    """
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'CogInsertFail, {0} '.format(self.message)
        else:
            return 'CogInsertFail has been raised'

class PrefixError(Exception):
    """
    Raised if unable to get a prefix
    """
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'PrefixError, {0} '.format(self.message)
        else:
            return 'PrefixError has been raised'