"""
Database query functions for cogs
"""
from util.db.query import query
from util.log import runLog
from util import exceptions

def loaded(name: str):
    """
    Gets is_loaded for cog
    :param int name: Name of cog
    :return: True if enabled
    :rtype: bool
    :raises CogNotFound: if unable to find cog in db
    """
    try:
        q = f"""SELECT is_loaded FROM `cogs` WHERE cog_name = '{name}'"""
        data = query.query(q)
    except exceptions.dbQueryFail:
        runLog.error("Failed to check for is_loaded cog. dbQueryFail (queryCog.loaded)")
        raise exceptions.CogNotFound
    else:
        if len(data) == 0:
            return False
        for i in data:
            return bool(i[0])

def enabled(name: str):
    """
    Gets is_enabled for cog
    :param int name: Name of cog
    :return: True if enabled
    :rtype: bool
    :raises CogNotFound: if unable to find cog in db
    """
    try:
        q = f"""SELECT is_enabled FROM `cogs` WHERE cog_name = '{name}'"""
        data = query.query(q)
    except exceptions.dbQueryFail:
        runLog.error("Failed to check for is_enabled cog. dbQueryFail (queryCog.enabled)")
        raise exceptions.CogNotFound
    else:
        if len(data) == 0:
            return False
        for i in data:
            return bool(i[0])