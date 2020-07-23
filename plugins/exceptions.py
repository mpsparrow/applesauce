from utils.logger import log

class pluginTableError(PluginError):
    """
    Raised when there is an error accessing a config file
    """
    def __init__(self, name, error):
        self.name = name
        self.error = error

    def __str__(self):
        log.error(f"{self.name}: pluginTableError: {self.error}")
        return f"{self.name}: pluginTableError: {self.error}"