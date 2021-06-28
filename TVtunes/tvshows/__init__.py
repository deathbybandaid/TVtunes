import time

from TVtunes.tools import humanized_time

from .tvshow import TVShow


class TVShows():
    """
    Methods for Managing Plex shows, Shows, and their Theme Music.
    """

    def __init__(self, tvtunes, plexinterface):
        self.tvtunes = tvtunes
        self.plexinterface = plexinterface

        self.list = {}

        self.get_db_shows()

        self.shows_update_url = "/api/tvshows?method=scan"
        self.tvtunes.scheduler.every(4).to(5).hours.do(self.tvtunes.api.threadget, url=self.shows_update_url)

    def get_db_shows(self):
        """
        Retrieve existing shows from database.
        """

        self.tvtunes.logger.info("Checking for Shows information stored in the database.")
        shows_ids = self.tvtunes.db.get_tvtunes_value("shows", "list") or []

        if len(shows_ids):
            self.tvtunes.logger.info("Found %s existing shows in the database." % str(len(shows_ids)))

        for show_id in shows_ids:
            tvshow_obj = TVShow(self.tvtunes, self.plexinterface, show_id=show_id)
            show_id = tvshow_obj.dict["id"]
            self.list[show_id] = tvshow_obj

    def get_shows(self, forceupdate=False):
        """
        Pull shows from Plex.
        """

        return_show_list = []
        if not len(list(self.list.keys())):
            self.get_db_shows()

        if not forceupdate:
            return_show_list.extend([self.list[x].dict for x in list(self.list.keys())])

        else:

            show_id_list = [str(self.list[x].dict["plex_id"]) for x in list(self.list.keys())]

            if self.tvtunes.config.dict["logging"]["level"].upper() == "NOOB":
                self.tvtunes.logger.noob("Performing Shows Scan. This Process can take some time, Please Wait.")
            else:
                self.tvtunes.logger.info("Performing Shows Scan.")

            show_scan_start = time.time()

            self.tvtunes.logger.info("Found a Total of %s Libraries" % self.plexinterface.total_libraries)

            self.tvtunes.logger.info("Found %s TV Shows in %s Libraries" % (self.plexinterface.total_tv_shows, self.plexinterface.total_tv_libraries))

            list_library_shows_all = self.plexinterface.list_library_shows_all

            newshow = 0
            for tvshow_info in list_library_shows_all:

                show_id = tvshow_info.guid

                show_existing = str(show_id) in show_id_list

                if show_existing:
                    self.tvtunes.logger.debug("Found Existing show: %s" % tvshow_info.title)
                    tvshow_obj = self.get_show_obj("show_id", show_id)

                else:
                    self.tvtunes.logger.debug("Creating new show: %s" % tvshow_info.title)
                    tvshow_obj = TVShow(self.tvtunes, self.plexinterface, show_id=show_id)

                if not show_existing:
                    self.list[show_id] = tvshow_obj
                    newshow += 1

                tvshow_obj.basics(tvshow_info)

            self.tvtunes.logger.info("Shows Import took %s" % (humanized_time(time.time() - show_scan_start)))

            if not newshow:
                newshow = "no"
            self.tvtunes.logger.info("Found %s NEW shows." % newshow)

        self.tvtunes.logger.info("Total Show Count: %s" % len(self.list.keys()))
        self.save_db_shows()

        self.tvtunes.db.set_tvtunes_value("shows", "scanned_time", time.time())
        return_show_list.extend([self.list[x].dict for x in list(self.list.keys())])

        return return_show_list

    def get_show_obj(self, keyfind, valfind):
        """
        Retrieve show object by keyfind property.
        """

        matches = [self.list[x].dict["id"] for x in list(self.list.keys()) if self.list[x].dict[keyfind] == valfind]

        if len(matches):
            return self.list[matches[0]]

        return None

    def save_db_shows(self, origin=None):
        """
        Save Show listing to the database.
        """

        self.tvtunes.logger.debug("Saving shows to database.")
        show_ids = [self.list[x].dict["id"] for x in list(self.list.keys())]
        self.tvtunes.db.set_tvtunes_value("shows", "list", show_ids)
