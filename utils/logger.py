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


def createFolder(name: str):
    """
    Create a folder
    """
    if not(os.path.isdir(name)):
        os.mkdir(name)

def clearLogs():
    """
    Cleans main logs and makes sure folder structure is correct
    """
    if os.path.isdir("logs"):
        logFiles = [f for f in os.listdir("logs") if os.path.isfile(join("logs", f))]
        
        for logFile in logFiles:
            try:
                with open(logFile, "w"):
                    pass
            except Exception as error:
                pass