
from .root_url import Root_URL
from .startup_tasks import Startup_Tasks

from .settings import Settings
from .logs import Logs
from .versions import Versions
from .tvshows import TVShows
from .debug import Debug_JSON
from .route_list import Route_List


class TVtunes_API():

    def __init__(self, tvtunes):
        self.tvtunes = tvtunes

        self.root_url = Root_URL(tvtunes)
        self.startup_tasks = Startup_Tasks(tvtunes)
        self.settings = Settings(tvtunes)
        self.logs = Logs(tvtunes)
        self.versions = Versions(tvtunes)
        self.debug = Debug_JSON(tvtunes)
        self.route_list = Route_List(tvtunes)

        self.tvshows = TVShows(tvtunes)
