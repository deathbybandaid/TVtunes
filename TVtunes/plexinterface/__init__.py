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

        first_show_lib = self.list_tv_libraries[0]
        first_show = self.list_library_shows(first_show_lib)[0]
        # print(dir(first_show))
        """
        ['METADATA_TYPE', 'TAG', 'TYPE', '_INCLUDES', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_autoReload', '_buildDetailsKey', '_buildItem', '_buildItemOrNone', '_castAttrValue', '_checkAttrs', '_clean', '_data', '_defaultSyncTitle', '_details_key', '_edit_tags', '_getAttrOperator', '_getAttrValue', '_initpath', '_isChildOf', '_loadData', '_manuallyLoadXML', '_parent', '_reload', '_server', 'actors', 'addCollection', 'addGenre', 'addLabel', 'addedAt', 'analyze', 'art', 'artBlurHash', 'artUrl', 'arts', 'audienceRating', 'audienceRatingImage', 'augmentation', 'autoDeletionItemPolicyUnwatchedLibrary', 'autoDeletionItemPolicyWatchedLibrary', 'banner', 'bannerUrl', 'banners', 'childCount', 'collections', 'contentRating', 'defaultAdvanced', 'delete', 'download', 'duration', 'edit', 'editAdvanced', 'episode', 'episodeSort', 'episodes', 'fetchItem', 'fetchItems', 'fields', 'findItems', 'firstAttr', 'fixMatch', 'flattenSeasons', 'genres', 'get', 'guid', 'guids', 'history', 'hubs', 'index', 'isFullObject', 'isPartialObject', 'isWatched', 'key', 'labels', 'languageOverride', 'lastRatedAt', 'lastViewedAt', 'leafCount', 'librarySectionID', 'librarySectionKey', 'librarySectionTitle', 'listAttrs', 'listType', 'locations', 'markUnwatched', 'markWatched', 'matches', 'merge', 'network', 'onDeck', 'optimize', 'originalTitle', 'originallyAvailableAt', 'posterUrl', 'posters', 'preference', 'preferences', 'rate', 'rating', 'ratingKey', 'refresh', 'reload', 'removeCollection', 'removeGenre', 'removeLabel', 'removeSubtitles', 'roles', 'season', 'seasons', 'section', 'setArt', 'setBanner', 'setPoster', 'showOrdering', 'similar', 'split', 'studio', 'subtitleStreams', 'summary', 'sync', 'tagline', 'theme', 'thumb', 'thumbBlurHash', 'thumbUrl', 'title', 'titleSort', 'type', 'unmatch', 'unwatched', 'updatedAt', 'uploadArt', 'uploadBanner', 'uploadPoster', 'uploadSubtitles', 'url', 'useOriginalTitle', 'userRating', 'viewCount', 'viewedLeafCount', 'watched', 'year']
        """
        print(first_show.locations)

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
            return [x.title for x in self.plexserver.library.sections() if x.type == "show"]

    @property
    def total_tv_shows(self):
        if not self.plexserver:
            return 0
        else:
            total_shows = 0
            for x in self.list_tv_libraries:
                total_shows += len(self.list_library_shows(x))
            return total_shows

    def list_library_shows(self, library):
        return self.plexserver.library.section(library).all()

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
