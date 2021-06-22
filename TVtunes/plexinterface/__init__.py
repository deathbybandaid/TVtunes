

class PlexInterface():
    """
    Methods for Connecting to a Plex Server.
    """

    def __init__(self, tvtunes):
        self.tvtunes = tvtunes
        self.config = self.tvtunes.config

        self.setup_success = False
        self.connect()

    def connect(self):
        self.tvtunes.logger.info("Attempting Connection to Plex Media Server at %s:%s" % (self.address, self.port))
        self.tvtunes.logger.info("Plex Connection Setup Success")
        self.setup_success = True

    @property
    def address(self):
        """
        Address of Plex Server.
        """

        return self.config.dict["plex"]["address"]

    @property
    def port(self):
        """
        Port of Plex Server.
        """

        return self.config.dict["plex"]["port"]

    @property
    def token(self):
        """
        Token for Plex Server.
        """

        return self.config.dict["plex"]["token"]
