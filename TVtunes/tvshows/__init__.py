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
            show_id_obj = TVShow(self.tvtunes, self.plexinterface, show_id=show_id)
            show_id = show_id_obj.dict["id"]
            self.list[show_id] = show_id_obj

    def get_shows(self, forceupdate=False):
        """
        Pull shows from Plex.
        """

        return_lib_list = []
        if not len(list(self.list.keys())):
            self.get_db_shows()

        if not forceupdate:
            return_lib_list.extend([self.list[x].dict for x in list(self.list.keys())])

        else:

            if self.tvtunes.config.dict["logging"]["level"].upper() == "NOOB":
                self.tvtunes.logger.noob("Performing Shows Scan. This Process can take some time, Please Wait.")
            else:
                self.tvtunes.logger.info("Performing Shows Scan.")

            show_scan_start = time.time()

            self.tvtunes.logger.info("Found %s Libraries" % self.plexinterface.total_libraries)

            self.tvtunes.logger.info("Found a %s TV Show Libaries" % self.plexinterface.total_tv_libraries)

            self.tvtunes.logger.info("Found a %s TV Shows" % self.plexinterface.total_tv_shows)

            list_library_shows_all = self.plexinterface.list_library_shows_all
            print(list_library_shows_all[0])

            self.tvtunes.logger.info("Shows Import took %s" % (humanized_time(time.time() - show_scan_start)))

        return
