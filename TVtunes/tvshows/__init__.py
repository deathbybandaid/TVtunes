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
            print(list_library_shows_all[0].librarySectionTitle)
            print(list_library_shows_all[0].title)
            print(list_library_shows_all[0].ratingKey)
            print(list_library_shows_all[0].theme.split("/")[-1])

            for x in list_library_shows_all[0].guids:
                print(dir(x))

            print(self.plexinterface.show_theme_url(list_library_shows_all[0].librarySectionTitle, list_library_shows_all[0].title))

            self.tvtunes.logger.info("Shows Import took %s" % (humanized_time(time.time() - show_scan_start)))

        return


"""
[
'METADATA_TYPE',
'TAG',
'TYPE',
'_INCLUDES', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_autoReload', '_buildDetailsKey', '_buildItem', '_buildItemOrNone', '_castAttrValue', '_checkAttrs', '_clean', '_data', '_defaultSyncTitle', '_details_key', '_edit_tags', '_getAttrOperator', '_getAttrValue', '_initpath', '_isChildOf', '_loadData', '_manuallyLoadXML', '_parent', '_reload', '_server', 'actors', 'addCollection', 'addGenre', 'addLabel', 'addedAt', 'analyze', 'art', 'artBlurHash', 'artUrl', 'arts', 'audienceRating', 'audienceRatingImage', 'augmentation', 'autoDeletionItemPolicyUnwatchedLibrary', 'autoDeletionItemPolicyWatchedLibrary', 'banner', 'bannerUrl', 'banners', 'childCount', 'collections', 'contentRating', 'defaultAdvanced', 'delete', 'download', 'duration', 'edit', 'editAdvanced', 'episode', 'episodeSort', 'episodes', 'fetchItem', 'fetchItems', 'fields', 'findItems', 'firstAttr', 'fixMatch', 'flattenSeasons', 'genres', 'get', 'guid', 'guids', 'history', 'hubs', 'index', 'isFullObject', 'isPartialObject', 'isWatched', 'key', 'labels', 'languageOverride', 'lastRatedAt', 'lastViewedAt', 'leafCount', 'librarySectionID', 'librarySectionKey', 'librarySectionTitle', 'listAttrs', 'listType', 'locations', 'markUnwatched', 'markWatched', 'matches', 'merge', 'network', 'onDeck', 'optimize', 'originalTitle', 'originallyAvailableAt', 'posterUrl', 'posters', 'preference', 'preferences', 'rate', 'rating', 'ratingKey', 'refresh', 'reload', 'removeCollection', 'removeGenre', 'removeLabel', 'removeSubtitles', 'roles', 'season', 'seasons', 'section', 'setArt', 'setBanner', 'setPoster', 'showOrdering', 'similar', 'split', 'studio', 'subtitleStreams', 'summary', 'sync', 'tagline', 'theme', 'thumb', 'thumbBlurHash', 'thumbUrl', 'title', 'titleSort', 'type', 'unmatch', 'unwatched', 'updatedAt', 'uploadArt', 'uploadBanner', 'uploadPoster', 'uploadSubtitles', 'url', 'useOriginalTitle', 'userRating', 'viewCount', 'viewedLeafCount', 'watched', 'year']
"""


"https://10-0-12-90.b80992c7ee74434aaff6dec85bd543a7.plex.direct:32400/library/metadata/13878/theme/1615171270?X-Plex-Product=Plex%20Web&X-Plex-Version=4.59.2&X-Plex-Client-Identifier=ffetlvpts1qt7eom8n7zqwpk&X-Plex-Platform=Chrome&X-Plex-Platform-Version=92.0&X-Plex-Sync-Version=2&X-Plex-Features=external-media%2Cindirect-media&X-Plex-Model=hosted&X-Plex-Device=Windows&X-Plex-Device-Name=Chrome&X-Plex-Device-Screen-Resolution=2133x1052%2C1920x1080&X-Plex-Token=NuL9SLyHQCb1tqqYsKiZ&X-Plex-Language=en&Accept-Language=en"

"https://10-0-12-90.b80992c7ee74434aaff6dec85bd543a7.plex.direct:32400/library/metadata/13878/theme/1615171270?X-Plex-Token=NuL9SLyHQCb1tqqYsKiZ"
