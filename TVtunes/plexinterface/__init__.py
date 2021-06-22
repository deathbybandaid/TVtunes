import plexapi
from plexapi.server import PlexServer


class PlexInterface():
    """
    Methods for Connecting to a Plex Server.
    """

    def __init__(self, tvtunes):
        self.tvtunes = tvtunes
        self.config = self.tvtunes.config

        self.plexserver = None
        self.tv_libraries = {}
        self.connect()

    def connect(self):
        self.tvtunes.logger.info("Attempting Connection to Plex Media Server at %s:%s" % (self.address, self.port))

        try:
            self.plexserver = PlexServer(self.baseurl, self.token)
        except plexapi.exceptions.Unauthorized:
            self.plexserver = None
            self.tvtunes.logger.error("Plex Connection Setup Failed: Unauthorized")
            return
        except Exception as err:
            self.plexserver = None
            self.tvtunes.logger.error("Plex Connection Setup Failed: Unable to Connect %s" % err)
            return

        self.tvtunes.logger.info("Retrieving Library list.")
        self.tv_libraries = {}

        self.tvtunes.logger.info("Found a total of %s Libaries" % len(self.plexserver.library.sections()))

        self.tvtunes.logger.info("Found a total of %s TV Show Libaries" % len([x for x in self.plexserver.library.sections() if x.type == "show"]))

        print(self.plexserver.library.section(self.plexserver.library.sections()[0].title))

        # self.tvtunes.logger.info("Found a total of %s TV Shows" % len(self.tv_libraries.keys()))

    @property
    def baseurl(self):
        """
        Base URL of Plex Server.
        """

        return "http://%s:%s" % (self.address, self.port)

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
