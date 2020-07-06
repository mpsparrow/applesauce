"""
Database table creation functions
"""
from util.db import commit
from util import exceptions

def prefix():
    """
    Creates 'prefix' database table
    :raises dbTableFail: if query fails to create table
    """
    try:
        table = """CREATE TABLE `prefix` (
                `guild_id` BIGINT NOT NULL,
                `prefix` CHAR(50) NOT NULL,
                primary key (guild_id)
                )"""
        commit.commit(table)
    except exceptions.dbQueryFail:
        raise exceptions.dbTableFail("prefix table unable to be created (util.db.tables.prefix)")

def ignore():
    """
    Creates 'ignore' database table
    :raises dbTableFail: if query fails to create table
    """
    try:
        table = """CREATE TABLE `ignore` (
                `guild_id` BIGINT NOT NULL,
                `guild_name` VARCHAR(50) NOT NULL,
                `member_id` BIGINT NOT NULL, 
                `is_ignored` BOOLEAN NOT NULL,
                primary key (guild_id, member_id)
                )"""
        commit.commit(table)
    except exceptions.dbQueryFail:
        raise exceptions.dbTableFail("ignore table unable to be created (util.db.tables.ignore)")

def cogsList():
    """
    Creates 'cogs_list' database table (for keeping of main cog states)
    :raises dbTableFail: if query fails to create table
    """
    try:
        table = """CREATE TABLE `cogs_list` (
                `cog_name` VARCHAR(50) NOT NULL,
                `is_enabled` BOOLEAN,
                `is_loaded` BOOLEAN,
                primary key (cog_name)
                )"""
        commit.commit(table)
    except exceptions.dbQueryFail:
        raise exceptions.dbTableFail("cogsList table unable to be created (util.db.tables.cogsList)")

def cogsGuild():
    """
    Creates 'cogs_guild' database table (for each guild)
    :raises dbTableFail: if query fails to create table
    """
    try:
        table = """CREATE TABLE `cogs_guild` (
                `guild_id` BIGINT NOT NULL,
                `cog_name` VARCHAR(30) NOT NULL,
                `is_enabled` BOOLEAN NOT NULL,
                primary key (guild_id, cog_name)
                )"""
        commit.commit(table)
    except exceptions.dbQueryFail:
        raise exceptions.dbTableFail("cogsGuild table unable to be created (util.db.tables.cogsGuild)")

def config():
    """
    Creates 'config' database table
    :raises dbTableFail: if query fails to create table
    """
    try:
        table = """CREATE TABLE `config` (
                `guild_id` BIGINT NOT NULL,
                `option_name` VARCHAR(50) NOT NULL,
                `value` LONGTEXT NOT NULL,
                primary key (guild_id, option_name)
                )"""
        commit.commit(table)
    except exceptions.dbQueryFail:
        raise exceptions.dbTableFail("config table unable to be created (util.db.tables.config)")

def channel():
    """
    Creates 'channel' database table
    :raises dbTableFail: if query fails to create table
    """
    try:
        table = """CREATE TABLE `channel` (
                `channel_id` BIGINT NOT NULL,
                `guild_id` BIGINT NOT NULL,
                `option_name` VARCHAR(50) NOT NULL,
                `is_enabled` BOOLEAN NOT NULL,
                primary key (channel_id, guild_id, option_name)
                )"""
        commit.commit(table)
    except exceptions.dbQueryFail:
        raise exceptions.dbTableFail("channel table unable to be created (util.db.tables.channel)")

def archive():
    """
    Creates 'archive' database table
    :raises dbTableFail: if query fails to create table
    """
    try:
        table = """CREATE TABLE `archive` (
                `guild_id` BIGINT NOT NULL,
                `channel` BIGINT,
                `role` BIGINT,
                `pins` BOOLEAN,
                `toggle` BOOLEAN,
                primary key (guild_id)
                )"""
        commit.commit(table)
    except exceptions.dbQueryFail:
        raise exceptions.dbTableFail("archive table unable to be created (util.db.tables.archive)")

def leaderboard():
    """
    Creates 'leaderboard' database table
    :raises dbTableFail: if query fails to create table
    """
    try:
        table = """CREATE TABLE `leaderboard` (
                `guild_id` BIGINT NOT NULL,
                `guild_name` VARCHAR(50) NOT NULL,
                `member_id` BIGINT NOT NULL,
                `member_name` VARCHAR(50),
                `level` INT,
                `points` BIGINT,
                `next_level` BIGINT,
                `last_added` DATETIME,
                `message_count` BIGINT,
                primary key (guild_id, member_id)
                )"""
        commit.commit(table)
    except exceptions.dbQueryFail:
        raise exceptions.dbTableFail("leaderboard table unable to be created (util.db.tables.leaderboard)")