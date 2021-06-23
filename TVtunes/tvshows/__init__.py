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

            self.tvtunes.logger.info("Found a Total of %s Libraries" % self.plexinterface.total_libraries)

            self.tvtunes.logger.info("Found %s TV Shows in %s Libraries" % (self.plexinterface.total_tv_shows, self.plexinterface.total_tv_libraries))

            list_library_shows_all = self.plexinterface.list_library_shows_all
            print(list_library_shows_all[0].title)
            tvdb_id = list_library_shows_all[0].episodes()[0].guid.split('/')[2]
            print(tvdb_id)
            print(list_library_shows_all[0].librarySectionTitle)

            self.tvtunes.logger.info("Shows Import took %s" % (humanized_time(time.time() - show_scan_start)))

        return


"""
['METADATA_TYPE', 'TAG', 'TYPE', '_INCLUDES', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_autoReload', '_buildDetailsKey', '_buildItem', '_buildItemOrNone', '_castAttrValue', '_checkAttrs', '_clean', '_data', '_defaultSyncTitle', '_details_key', '_edit_tags', '_getAttrOperator', '_getAttrValue', '_initpath', '_isChildOf', '_loadData', '_manuallyLoadXML', '_parent', '_reload', '_server', 'actors', 'addCollection', 'addGenre', 'addLabel', 'addedAt', 'analyze', 'art', 'artBlurHash', 'artUrl', 'arts', 'audienceRating', 'audienceRatingImage', 'augmentation', 'autoDeletionItemPolicyUnwatchedLibrary', 'autoDeletionItemPolicyWatchedLibrary', 'banner', 'bannerUrl', 'banners', 'childCount', 'collections', 'contentRating', 'defaultAdvanced', 'delete', 'download', 'duration', 'edit', 'editAdvanced', 'episode', 'episodeSort', 'episodes', 'fetchItem', 'fetchItems', 'fields', 'findItems', 'firstAttr', 'fixMatch', 'flattenSeasons', 'genres', 'get', 'guid', 'guids', 'history', 'hubs', 'index', 'isFullObject', 'isPartialObject', 'isWatched', 'key', 'labels', 'languageOverride', 'lastRatedAt', 'lastViewedAt', 'leafCount', 'librarySectionID', 'librarySectionKey', 'librarySectionTitle', 'listAttrs', 'listType', 'locations', 'markUnwatched', 'markWatched', 'matches', 'merge', 'network', 'onDeck', 'optimize', 'originalTitle', 'originallyAvailableAt', 'posterUrl', 'posters', 'preference', 'preferences', 'rate', 'rating', 'ratingKey', 'refresh', 'reload', 'removeCollection', 'removeGenre', 'removeLabel', 'removeSubtitles', 'roles', 'season', 'seasons', 'section', 'setArt', 'setBanner', 'setPoster', 'showOrdering', 'similar', 'split', 'studio', 'subtitleStreams', 'summary', 'sync', 'tagline', 'theme', 'thumb', 'thumbBlurHash', 'thumbUrl', 'title', 'titleSort', 'type', 'unmatch', 'unwatched', 'updatedAt', 'uploadArt', 'uploadBanner', 'uploadPoster', 'uploadSubtitles', 'url', 'useOriginalTitle', 'userRating', 'viewCount', 'viewedLeafCount', 'watched', 'year']
"""
