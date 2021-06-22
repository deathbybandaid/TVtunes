from flask import send_from_directory

import pathlib


class Brython():
    endpoints = ["/brython.js"]
    endpoint_name = "file_brython_js"

    def __init__(self, tvtunes):
        self.tvtunes = tvtunes
        self.brython_path = pathlib.Path(self.tvtunes.config.internal["paths"]["TVtunes_web_dir"]).joinpath('brython')

    def __call__(self, *args):
        return self.get(*args)

    def get(self, *args):

        return send_from_directory(self.brython_path,
                                   'brython.js',
                                   mimetype='text/javascript')
