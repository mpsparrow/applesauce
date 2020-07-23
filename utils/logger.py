import logging
import os

# main format for logs
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

def setup_logger(name, log_file, level=logging.INFO, logFormat=formatter):
    """
    Creates new logging instances
    :param str name: unique name for logger
    :param str log_file: location of log file
    :param level: logging level
    :param format: logging format
    """
    handler = logging.FileHandler(log_file)        
    handler.setFormatter(logFormat)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# define log types
startLog = setup_logger('startLog', 'logs/startup.log')
log = setup_logger('log', 'logs/runtime.log')
pluginLog = setup_logger('pluginLog', 'logs/plugins.log')

logFiles = ["logs/discord.log", "logs/plugins.log", "logs/runtime.log", "logs/startup.log"]

def cleanLogs():
    """
    Cleans main logs and makes sure folder structure is correct
    """
    # create 'logs' folder
    try:
        os.mkdir("logs")
    except OSError:
        pass

    # clean log files
    for logFile in logFiles:
        try:
            with open(logFile, "w"):
                pass
        except Exception as error:
            pass