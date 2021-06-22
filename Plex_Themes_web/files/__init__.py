

from .favicon_ico import Favicon_ICO
from .style_css import Style_CSS


class TVtunes_Files():

    def __init__(self, tvtunes):
        self.tvtunes = tvtunes

        self.favicon = Favicon_ICO(tvtunes)
        self.style = Style_CSS(tvtunes)
