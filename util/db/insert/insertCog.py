from util.db import commit

def loaded(name: str, loaded: bool):
    """
    Sets cog is_loaded status in db.
    :param str name: Cog name
    :param bool loaded: Loaded cog status
    """
    query = f"""INSERT INTO `cogs` (
        cog_name, is_loaded
    ) VALUES (%s, %s) ON DUPLICATE KEY UPDATE is_loaded = VALUES(is_loaded)"""
    values = (name, loaded)
    commit.commit(query, values)

def enabled(name: str, enabled: bool):
    """
    Sets cog is_enabled status in db.
    :param str name: Cog name
    :param bool enabled: Enable on startup or not
    """
    query = f"""INSERT INTO `cogs` (
        cog_name, is_enabled
    ) VALUES (%s, %s) ON DUPLICATE KEY UPDATE is_enabled = VALUES(is_enabled)"""
    values = (name, enabled)
    commit.commit(query, values)