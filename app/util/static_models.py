class BotJobSM():
    """defines the structure of bot jobs

    Attributes
    ----------

    Methods
    -------

    """

    def __init__(self, taskId, taskVersionId, botSecretLists, parameters = ""):
        """constructor that defines the 
        """
        self.taskId = taskId
        self.taskVersionId = taskVersionId
        self.botSecretLists = botSecretLists
        self.parameters = parameters