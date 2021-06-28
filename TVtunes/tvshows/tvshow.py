

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
                "title": None
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

        self.dict["library"] = tvshow_info.librarySectionTitle

        self.dict["title"] = tvshow_info.title

        self.dict["tvdbid"] = self.plexinterface.show_tvdbid(self.library, self.title)

        self.dict["directory"] = self.plexinterface.show_location(self.library, self.title)

    @property
    def pms_theme_url(self):
        return self.plexinterface.pms_theme_url(self.library, self.title)

    @property
    def plexcom_theme_url(self):
        if not self.tvdbid:
            return None
        return self.plexinterface.plexcom_theme_url(self.tvdbid)

    @property
    def theme_file(self):
        return "%s/theme.mp3" % self.directory

    @property
    def theme_file_cache(self):
        if not self.tvdbid:
            return None
        return "%s/%s.mp3" % (self.tvtunes.config.internal["paths"]["mp3_dir"], self.tvdbid)

    def __getattr__(self, name):
        """
        Quick and dirty shortcuts. Will only get called for undefined attributes.
        """

        if name in list(self.dict.keys()):
            return self.dict[name]

        else:
            return None
