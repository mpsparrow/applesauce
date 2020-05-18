"""
Custom throwable exceptions
"""

class ApplesauceError(Exception):
    """
    Base exception for all other Applesauce exceptions
    """
    pass

class dbConnectionFail(Exception):
    """
    Raised when database connection fails
    """
    pass

class dbCommitFail(Exception):
    """
    Raised when database commit fails
    """
    pass

class dbQueryFail(Exception):
    """
    Raised when database query fails
    """
    pass

class dbTableCreationFail(Exception):
    """
    Raised when database table is unable to be created
    """
    pass

class configReadError(Exception):
    """
    Raised when there is an error reading a config file
    """
    pass

class configWriteError(Exception):
    """
    Raised when there is an error writing to a config file
    """
    pass

class CogNotFound(Exception):
    """
    Raised when cog is not found in db
    """
    pass

class CogInsertFail(Exception):
    """
    Raised when cog fails to be inserted into db
    """
    pass

class PrefixError(Exception):
    """
    Raised if unable to get a prefix
    """
    pass