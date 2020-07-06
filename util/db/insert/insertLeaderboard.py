"""
Database insertion functions for leaderboard
"""
from util.db import commit
from util.log import runLog
from util import exceptions

def leaderboard(guild_id: int, guild_name: str, member_id: int, member_name: str, level: int, points: int, next_level: int, last_added, message_count: int):
    try:
        query = f"""INSERT INTO `leaderboard` (
            guild_id, guild_name, member_id, member_name, level, points, next_level, last_added, message_count
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) 
            ON DUPLICATE KEY UPDATE 
            guild_name = VALUES(guild_name), 
            member_name = VALUES(member_name), 
            level = VALUES(level), 
            points = VALUES(points), 
            next_level = VALUES(next_level),
            last_added = VALUES(last_added),
            message_count = VALUES(message_count)"""
        values = (guild_id, guild_name, member_id, member_name, level, points, next_level, last_added, message_count)
    except:
        pass