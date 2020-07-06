"""
Main expections for bot framework
"""
from util.log import runLog

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
            runLog.error(f"dbConnectionFail, {self.message}")
            return f"dbConnectionFail, {self.message}"
        runLog.error("dbConnectionFail has been raised")
        return "dbConnectionFail has been raised"

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
            runLog.error(f"dbCommitFail, {self.message}")
            return f"dbCommitFail, {self.message}"
        runLog.error("dbCommitFail has been raised")
        return "dbCommitFail has been raised"

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
            runLog.error(f"dbQueryFail, {self.message}")
            return f"dbQueryFail, {self.message}"
        runLog.error("dbQueryFail has been raised")
        return "dbQueryFail has been raised"

class dbTableFail(Exception):
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
            runLog.error(f"dbTableFail, {self.message}")
            return f"dbTableFail, {self.message}"
        runLog.error("dbTableFail has been raised")
        return "dbTableFail has been raised"

class configError(Exception):
    """
    Raised when there is an error accessing a config file
    """
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            runLog.error(f"configError, {self.message}")
            return f"configError, {self.message}"
        runLog.error("configError has been raised")
        return "configError has been raised"

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
            runLog.error(f"PrefixError, {self.message}")
            return f"PrefixError, {self.message}"
        runLog.error("PrefixError has been raised")
        return "PrefixError has been raised"