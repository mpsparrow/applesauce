from .manage import Manage
# from utils.database.actions import commit
# from plugins.exceptions import pluginTableError

### PLUGIN INFO ###
PLUGIN_NAME = "Plugin Management"
COG_NAMES = ["Manage"]
VERSION = 0.1
AUTHOR = "Matthew Sparrow"
DESCRIPTION = "Provides the basic per guild management features for enabling/disabling plugins."


def createTable():
    """
    Creates database table for plugin
    """
    table = """CREATE TABLE `plugins_guild` (
            `guild_id` BIGINT NOT NULL,
            `plugin_name` VARCHAR(255) NOT NULL,
            `enabled` BOOLEAN NOT NULL,
            primary key (guild_id, cog_name)
            )"""
    # commit(table)

def setup(bot):
    """
    Setup when registering plugin
    :raises PluginTableError: database table errored out while being created

    try:
        # create database table for plugin
        create_table()
    except Exception as error:
        # raised if database table errored out while being created
        raise PluginTableError(PLUGIN_NAME, error)
    """
    
    # register cog
    bot.add_cog(Manage(bot))