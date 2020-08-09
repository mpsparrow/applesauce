import logging
import os

# main format for logs
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s (%(pathname)s - %(funcName)s - %(lineno)d)")

def setup_logger(name, log_file, level=logging.DEBUG, logFormat=formatter):
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
startLog = setup_logger("startLog", "logs/startup.log", logFormat=logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
log = setup_logger("log", "logs/runtime.log")
pluginLog = setup_logger("pluginLog", "logs/plugins.log", logFormat=logging.Formatter("%(asctime)s %(levelname)s %(message)s"))

def clearLogs():
    """
    Cleans main logs and makes sure folder structure is correct
    """
    if os.path.isdir("logs"):
        logFiles = [f for f in os.listdir("logs") if os.path.isfile(os.path.join("logs", f))]

        for logFile in logFiles:
            try:
                with open(f"logs/{logFile}", "w"):
                    pass
            except IOError:
                log.exception("failed clearing logs")