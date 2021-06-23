import plexapi
from plexapi.server import PlexServer


class PlexInterface():
    """
    Methods for Connecting to a Plex Server.
    """

    def __init__(self, tvtunes):
        self.tvtunes = tvtunes
        self.config = self.tvtunes.config

        self.plexserver = self.connect()
        self.log_whats_found()

    def connect(self):
        self.tvtunes.logger.info("Attempting Connection to Plex Media Server at %s:%s" % (self.address, self.port))

        try:
            plexserver = PlexServer(self.baseurl, self.token)
        except plexapi.exceptions.Unauthorized:
            self.tvtunes.logger.error("Plex Connection Setup Failed: Unauthorized")
            return None
        except Exception as err:
            self.tvtunes.logger.error("Plex Connection Setup Failed: Unable to Connect %s" % err)
            return None
        return plexserver

    def log_whats_found(self):
        self.tvtunes.logger.info("Retrieving Library list.")

        self.tvtunes.logger.info("Found %s Libraries" % self.total_libraries)

        self.tvtunes.logger.info("Found a %s TV Show Libaries" % self.total_tv_libraries)

        self.tvtunes.logger.info("Found a %s TV Shows" % self.total_tv_shows)

    @property
    def total_libraries(self):
        if not self.plexserver:
            return 0
        else:
            return len(self.plexserver.library.sections())

    @property
    def total_tv_libraries(self):
        if not self.plexserver:
            return 0
        else:
            return len([x for x in self.plexserver.library.sections() if x.type == "show"])

    @property
    def list_tv_libraries(self):
        if not self.plexserver:
            return []
        else:
            return [x for x in self.plexserver.library.sections() if x.type == "show"]

    @property
    def total_tv_shows(self):
        for x in self.list_tv_libraries:
            print(self.list_library_shows(x))
        if not self.plexserver:
            return 0
        else:
            return 0

    def list_library_shows(self, library):
        return self.plexserver.library.section(self.plexserver.library.sections(library).title).all()

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
