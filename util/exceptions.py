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