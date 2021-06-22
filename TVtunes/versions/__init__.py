import os
import sys
import platform

from TVtunes import TVtunes_VERSION
from TVtunes.tools import is_docker


class Versions():
    """
    TVtunes versioning management system.
    """

    def __init__(self, settings, TVtunes_web, logger, web, db, scheduler):
        self.TVtunes_web = TVtunes_web
        self.logger = logger
        self.web = web
        self.db = db
        self.scheduler = scheduler

        self.github_org_list_url = "https://api.github.com/orgs/TVtunes/repos?type=all"
        self.github_tvtunes_core_info_url = "https://raw.githubusercontent.com/TVtunes/TVtunes/main/version.json"

        self.dict = {}

        self.register_tvtunes()

        self.register_env()

        self.get_online_versions()

        self.update_url = "/api/versions?method=check"

    def sched_init(self, tvtunes):
        """
        The Scheduled update method.
        """

        self.api = tvtunes.api
        self.scheduler.every(2).to(3).hours.do(self.sched_update)

    def sched_update(self):
        """
        Use an API thread to update Versions listing.
        """

        self.api.threadget(self.update_url)

    def get_online_versions(self):
        """
        Update Onling versions listing.
        """
        return

    def register_version(self, item_name, item_version, item_type):
        """
        Register a version item.
        """

        self.logger.debug("Registering %s item: %s %s" % (item_type, item_name, item_version))
        self.dict[item_name] = {
                                "name": item_name,
                                "version": item_version,
                                "type": item_type
                                }

    def register_tvtunes(self):
        """
        Register core version items.
        """

        self.register_version("TVtunes", TVtunes_VERSION, "TVtunes")
        self.register_version("TVtunes_web", self.TVtunes_web.TVtunes_web_VERSION, "TVtunes")

    def register_env(self):
        """
        Register env version items.
        """

        self.register_version("Python", sys.version, "env")
        if sys.version_info.major == 2 or sys.version_info < (3, 7):
            self.logger.error('Error: TVtunes requires python 3.7+. Do NOT expect support for older versions of python.')

        opersystem = platform.system()
        self.register_version("Operating System", opersystem, "env")

        if opersystem in ["Linux", "Darwin"]:

            # Linux/Mac
            if os.getuid() == 0 or os.geteuid() == 0:
                self.logger.warning('Do not run TVtunes with root privileges.')

        elif opersystem in ["Windows"]:

            # Windows
            if os.environ.get("USERNAME") == "Administrator":
                self.logger.warning('Do not run TVtunes as Administrator.')

        else:
            self.logger.warning("Uncommon Operating System, use at your own risk.")

        isdocker = is_docker()
        self.register_version("Docker", isdocker, "env")
