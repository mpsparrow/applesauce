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
        q = f"""SELECT is_loaded FROM `cogs_list` WHERE cog_name = '{name}'"""
        data = query.query(q)
    except exceptions.dbQueryFail:
        raise exceptions.CogNotFound("Failed to check for is_loaded cog. Raised from dbQueryFail (util.db.query.queryCogList.loaded)")
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
        q = f"""SELECT is_enabled FROM `cogs_list` WHERE cog_name = '{name}'"""
        data = query.query(q)
    except exceptions.dbQueryFail:
        raise exceptions.CogNotFound("Failed to check for is_enabled cog. Raised from dbQueryFail (util.db.query.queryCogList.enabled)")
    else:
        if len(data) == 0:
            return False
        for i in data:
            return bool(i[0])