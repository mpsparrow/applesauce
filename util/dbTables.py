# Creation of database tables.
from util import dbConnect


# Prefix table for per guild prefix keeping
def prefix():
    cnx = dbConnect.connect()
    cursor = cnx.cursor()
    cursor.execute("""CREATE TABLE `prefix` (
        `guild_id` BIGINT NOT NULL,
        `prefix` CHAR(50) NOT NULL,
        primary key (guild_id)
        )""")

# Ignore table for per guild ignoring of users
def ignore():
    cnx = dbConnect.connect()
    cursor = cnx.cursor()
    cursor.execute("""CREATE TABLE `ignore` (
        `guild_id` BIGINT NOT NULL,
        `member_id` BIGINT NOT NULL, 
        `is_ignored` BOOLEAN NOT NULL,
        primary key (guild_id, member_id)
        )""")

# Commands table for per guild command enable/disable
def commands():
    cnx = dbConnect.connect()
    cursor = cnx.cursor()
    cursor.execute("""CREATE TABLE `commands` (
        `guild_id` BIGINT NOT NULL,
        `command_name` VARCHAR(30) NOT NULL, 
        `is_enabled` BOOLEAN NOT NULL,
        `times_used` BIGINT,
        primary key (guild_id, command_name)
        )""")

# Cogs table for which cogs to load and skip
def cogs():
    cnx = dbConnect.connect()
    cursor = cnx.cursor()
    cursor.execute("""CREATE TABLE `cogs` (
        `cog_name` VARCHAR(50) NOT NULL,
        `is_enabled` BOOLEAN NOT NULL,
        `is_loaded` BOOLEAN NOT NULL,
        primary key (cog_name)
        )""")

# Configuration table for per guild settings
def config():
    cnx = dbConnect.connect()
    cursor = cnx.cursor()
    cursor.execute("""CREATE TABLE `config` (
        `guild_id` BIGINT NOT NULL,
        `option_name` VARCHAR(50) NOT NULL,
        `value` LONGTEXT NOT NULL,
        primary key (guild_id, option_name)
        )""")

# Archiving table for per guild archiving settings
def archive():
    cnx = dbConnect.connect()
    cursor = cnx.cursor()
    cursor.execute("""CREATE TABLE `archive` (
        `guild_id` BIGINT NOT NULL,
        `channel` BIGINT,
        `role` BIGINT,
        `pins` BOOLEAN,
        `toggle` BOOLEAN,
        primary key (guild_id)
        )""")