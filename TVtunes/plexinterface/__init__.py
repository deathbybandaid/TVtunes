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

    @property
    def total_libraries(self):
        if not self.plexserver:
            return 0

        return len(self.plexserver.library.sections())

    @property
    def total_tv_libraries(self):
        if not self.plexserver:
            return 0

        return len([x for x in self.plexserver.library.sections() if x.type == "show"])

    @property
    def list_tv_libraries(self):
        if not self.plexserver:
            return []

        return [x.title for x in self.plexserver.library.sections() if x.type == "show"]

    @property
    def total_tv_shows(self):
        if not self.plexserver:
            return 0

        total_shows = 0
        for x in self.list_tv_libraries:
            total_shows += len(self.list_library_shows(x))
        return total_shows

    def list_library_shows(self, library):
        if not self.plexserver:
            return []
        return self.plexserver.library.section(library).all()

    def show_location(self, library, show):
        if not self.plexserver:
            return None

        show_item = self.plexserver.library.section(library).get(show)
        return show_item.locations[0]

    @property
    def list_library_shows_all(self):
        if not self.plexserver:
            return []

        shows_list = []
        for library in self.list_tv_libraries:
            shows_list.extend(self.plexserver.library.section(library).all())
        return shows_list

    def pms_theme_url(self, library, show):
        if not self.plexserver:
            return None

        show_item = self.plexserver.library.section(library).get(show)

        if not show_item.theme:
            return None

        themeid = show_item.theme.split("/")[-1]
        return "%s/library/metadata/%s/theme/%s?X-Plex-Token=%s" % (self.baseurl, show_item.ratingKey, themeid, self.token)

    def plexcom_theme_url(self, tvdbid):
        return "http://tvthemes.plexapp.com/%s.mp3" % tvdbid

    def show_tvdbid(self, library, show):
        if not self.plexserver:
            return None

        show_item = self.plexserver.library.section(library).get(show)
        guids = [str(item_guid.id).split("tvdb://")[-1] for item_guid in show_item.guids if str(item_guid.id).startswith("tvdb")]
        if not len(guids):
            return None
        return guids[0]

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
