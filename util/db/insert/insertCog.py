"""
Database insertion functions for cogs
"""
from util.db import commit
from util.log import runLog
from util import exceptions

def cog(name: str, is_enabled: bool, is_loaded: bool):
    """
    Set cog is_enabled and is_loaded status in db.
    :param str name: Cog name
    :param bool is_enabled: Enable on startup or not
    :param bool is_loaded: Loaded cog status
    :raises raise CogInsertFail: if fails to insert/update cog info in db
    """
    try:
        query = f"""INSERT INTO `cogs` (
            cog_name, is_enabled, is_loaded
        ) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE is_enabled = VALUES(is_enabled), is_loaded = VALUES(is_loaded)"""
        values = (name, is_enabled, is_loaded)
        commit.commitV(query, values)
    except exceptions.dbCommitFail:
        runLog.error(f"Error setting {name} cog is_loading. dbCommitFail (insertCog.loaded)")
        raise exceptions.CogInsertFail

def loaded(name: str, is_loaded: bool):
    """
    Sets cog is_loaded status in db.
    :param str name: Cog name
    :param bool is_loaded: Loaded cog status
    :raises raise CogInsertFail: if fails to insert/update cog info in db
    """
    try:
        query = f"""INSERT INTO `cogs` (
                cog_name, is_loaded
                ) VALUES (%s, %s) ON DUPLICATE KEY UPDATE is_loaded = VALUES(is_loaded)"""
        values = (name, is_loaded)
        commit.commitV(query, values)
    except exceptions.dbCommitFail:
        runLog.error(f"Error setting {name} cog is_loading. dbCommitFail (insertCog.loaded)")
        raise exceptions.CogInsertFail

def enabled(name: str, is_enabled: bool):
    """
    Sets cog is_enabled status in db.
    :param str name: Cog name
    :param bool is_enabled: Enable on startup or not
    :raises raise CogInsertFail: if fails to insert/update cog info in db
    """
    try:
        query = f"""INSERT INTO `cogs` (
            cog_name, is_enabled
        ) VALUES (%s, %s) ON DUPLICATE KEY UPDATE is_enabled = VALUES(is_enabled)"""
        values = (name, is_enabled)
        commit.commitV(query, values)
    except exceptions.dbCommitFail:
        runLog.error(f"Error setting {name} cog is_enabled. dbCommitFail (insertCog.enabled)")
        raise exceptions.CogInsertFail