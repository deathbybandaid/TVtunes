

class TVShow():
    """
    Methods for Cataloging a Plex TV Show.
    """

    def __init__(self, tvtunes, plexinterface, show_id):

        self.tvtunes = tvtunes
        self.plexinterface = plexinterface

        self.show_id = show_id

        self.dict = self.tvtunes.db.get_tvtunes_value(str(show_id), "dict") or self.default_dict
        self.verify_dict()

        self.tvtunes.db.set_tvtunes_value(self.dict["id"], "dict", self.dict)

    @property
    def default_dict(self):
        """
        A default for how a show listing should appear.
        """

        return {
                "id": str(self.show_id),
                "name": None
                }

    def verify_dict(self):
        """
        Development Purposes.
        Add new Show dict keys.
        """

        return

    def basics(self, tvshow_info):
        """
        Some Show Information is Critical.
        """

        self.library = tvshow_info.librarySectionTitle
        print(self.library)

        self.show_title = tvshow_info.title
        print(self.show_title)

        self.tvdbid = self.plexinterface.show_tvdbid(self.library, self.show_title)
        print(self.tvdbid)

        self.show_directory = self.plexinterface.show_location(self.library, self.show_title)
        print(self.show_directory)
        self.theme_file_location = "%s/theme.mp3" % self.show_directory
        print(self.theme_file_location)

        self.theme_file_cache = "%s/%s.mp3" % (self.tvtunes.config.internal["paths"]["mp3_dir"], self.tvdbid)
        print(self.theme_file_cache)

        print(self.plexinterface.show_theme_url(self.library, self.show_title))
        print(self.plexinterface.tvdb_theme_url(self.tvdbid))

        return
