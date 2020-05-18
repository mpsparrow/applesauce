"""
Database table creation functions
"""
from util.db import commit
from util.log import runLog
from util import exceptions

def prefix():
    """
    Creates 'prefix' database table.
    """
    try:
        table = """CREATE TABLE `prefix` (
                `guild_id` BIGINT NOT NULL,
                `prefix` CHAR(50) NOT NULL,
                primary key (guild_id)
                )"""
        commit.commit(table)
    except exceptions.dbQueryFail:
        raise exceptions.dbTableCreationFail

def ignore():
    """
    Creates 'ignore' database table.
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
        raise exceptions.dbTableCreationFail

def commands():
    """
    Creates 'commands' database table.
    """
    try:
        table = """CREATE TABLE `commands` (
                `guild_id` BIGINT NOT NULL,
                `command_name` VARCHAR(30) NOT NULL, 
                `is_enabled` BOOLEAN NOT NULL,
                `times_used` BIGINT,
                primary key (guild_id, command_name)
                )"""
        commit.commit(table)
    except exceptions.dbQueryFail:
        raise exceptions.dbTableCreationFail

def cogs():
    """
    Creates 'cogs' database table.
    """
    try:
        table = """CREATE TABLE `cogs` (
                `cog_name` VARCHAR(50) NOT NULL,
                `is_enabled` BOOLEAN,
                `is_loaded` BOOLEAN,
                primary key (cog_name)
                )"""
        commit.commit(table)
    except exceptions.dbQueryFail:
        raise exceptions.dbTableCreationFail

def config():
    """
    Creates 'config' database table.
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
        raise exceptions.dbTableCreationFail

def archive():
    """
    Creates 'archive' database table.
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
        raise exceptions.dbTableCreationFail

def leaderboard():
    """
    Creates 'leaderboard' database table.
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
        raise exceptions.dbTableCreationFail