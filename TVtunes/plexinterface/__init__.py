import plexapi


class PlexInterface():
    """
    Methods for Connecting to a Plex Server.
    """

    def __init__(self, tvtunes):
        self.tvtunes = tvtunes
        self.config = self.tvtunes.config

        self.plex = None
        self.connect()

    def connect(self):
        self.tvtunes.logger.info("Attempting Connection to Plex Media Server at %s:%s" % (self.address, self.port))

        try:
            self.plex = plexapi.server.PlexServer("http://%s:%s" % (self.address, self.port), "fart")
        except plexapi.exceptions.Unauthorized:
            self.plex = None
            self.tvtunes.logger.error("Plex Connection Setup Failed: Unauthorized")

        self.tvtunes.logger.info("Plex Connection Setup Success")

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
