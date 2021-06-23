# coding=utf-8

from .tvshows import TVShows
from .api import TVtunes_API_URLs
from .plexinterface import PlexInterface

TVtunes_VERSION = "v0.9.0-beta"


class TVtunes_INT_OBJ():

    def __init__(self, settings, logger, db, versions, web, scheduler, deps):
        """
        An internal catalogue of core methods.
        """

        self.version = TVtunes_VERSION
        self.versions = versions
        self.config = settings
        self.logger = logger
        self.db = db
        self.web = web
        self.scheduler = scheduler
        self.deps = deps

        self.api = TVtunes_API_URLs(settings, self.web, versions, logger)

        self.threads = {}


class TVtunes_OBJ():

    def __init__(self, settings, logger, db, versions, web, scheduler, deps):
        """
        The Core Backend.
        """

        logger.info("Initializing TVtunes Core Functions.")
        self.tvtunes = TVtunes_INT_OBJ(settings, logger, db, versions, web, scheduler, deps)

        self.tvtunes.plexinterface = PlexInterface(self.tvtunes)

        self.tvshows = TVShows(self.tvtunes, self.tvtunes.plexinterface)

    def __getattr__(self, name):
        """
        Quick and dirty shortcuts. Will only get called for undefined attributes.
        """

        if hasattr(self.tvtunes, name):
            return eval("self.tvtunes.%s" % name)
