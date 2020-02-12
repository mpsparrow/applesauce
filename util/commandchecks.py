# Checks that run before each command is executed.
# Certain owner commands bypass this.
import logger, dbQuery, dbInsert

# If the user is set as ignored in the guild
def ignoreCheck(guildID: int, author: int):
    return not(dbQuery.ignore(guildID, author))

# If command is enabled in the guild it is being executed in
def commandCheck(guildID: int, name: str):
    return dbQuery.command(guildID, name)

# Main check
def isAllowed(ctx):
    try:
        guildID = ctx.guild.id
        name = ctx.command.qualified_name
        author = ctx.message.author.id
        value = commandCheck(guildID, name) and ignoreCheck(guildID, author)

        # Ups the command usage counter if command checks all pass
        if value:
            dbInsert.commandCount(guildID, name) 

        return value
    except Exception as e:
        logger.errorRun("commandchecks.py isAllowed - command check failure")
        logger.errorRun(e)
        return False