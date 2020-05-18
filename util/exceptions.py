"""
Custom throwable exceptions
"""

class ApplesauceError(Exception):
    """
    Base exception for all other Applesauce exceptions
    """
    pass

class dbConnectionFail(ApplesauceError):
    """
    Raised when database connection fails
    """
    pass

class dbCommitFail(ApplesauceError):
    """
    Raised when database commit fails
    """
    pass

class dbQueryFail(ApplesauceError):
    """
    Raised when database query fails
    """
    pass

class dbTableCreationFail(ApplesauceError):
    """
    Raised when database table is unable to be created
    """
    pass

class configReadError(ApplesauceError):
    """
    Raised when there is an error reading a config file
    """
    pass

class configWriteError(ApplesauceError):
    """
    Raised when there is an error writing to a config file
    """
    pass

class CogNotFound(ApplesauceError):
    """
    Raised when cog is not found in db
    """
    pass

class CogInsertFail(ApplesauceError):
    """
    Raised when cog fails to be inserted into db
    """
    pass

class PrefixError(ApplesauceError):
    """
    Raised if unable to get a prefix
    """
    pass