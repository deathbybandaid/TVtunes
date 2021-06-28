

from .index_html import Index_HTML
from .versions_html import Versions_HTML
from .diagnostics_html import Diagnostics_HTML
from .settings_html import Settings_HTML
from .tvshows_html import TVShows_HTML


class TVtunes_Pages():

    def __init__(self, tvtunes):
        self.tvtunes = tvtunes

        self.index_html = Index_HTML(tvtunes)
        self.versions_html = Versions_HTML(tvtunes)
        self.diagnostics_html = Diagnostics_HTML(tvtunes)
        self.settings_html = Settings_HTML(tvtunes)

        self.tvshows_html = TVShows_HTML(tvtunes)
