

from .brython import Brython
from .brython_stdlib import Brython_stdlib

from .brython_bry import Brython_bry


class TVtunes_Brython():

    def __init__(self, tvtunes):
        self.tvtunes = tvtunes

        self.brython = Brython(tvtunes)
        self.brython_stdlib = Brython_stdlib(tvtunes)

        self.brython_bry = Brython_bry(tvtunes)
