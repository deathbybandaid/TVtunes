from flask import Response
import pathlib
from io import StringIO


class Style_CSS():
    endpoints = ["/style.css"]
    endpoint_name = "file_style_css"

    def __init__(self, tvtunes):
        self.tvtunes = tvtunes

        self.internal_style_file = pathlib.Path(
            self.tvtunes.config.internal["paths"]["www_dir"]).joinpath('style.css')

        self.internal_style = StringIO()
        self.internal_style.write(open(self.internal_style_file).read())

        self.pull_external_theme()

    def pull_external_theme(self):
        self.external_style = None
        self.external_style_address = None
        if self.tvtunes.config.dict["web_ui"]["theme"]:
            if self.tvtunes.config.dict["web_ui"]["theme"].startswith(tuple(["http://", "https://"])):
                css_req = self.tvtunes.web.session.get(self.tvtunes.config.dict["web_ui"]["theme"])
                self.external_style = StringIO(css_req.text)
                self.external_style_address = self.tvtunes.config.dict["web_ui"]["theme"]

    def __call__(self, *args):
        return self.get(*args)

    def get(self, *args):

        main_output = StringIO()

        main_output.write(self.internal_style.getvalue())
        if self.tvtunes.config.dict["web_ui"]["theme"]:
            if self.tvtunes.config.dict["web_ui"]["theme"] != self.external_style_address:
                self.pull_external_theme()
            if self.external_style:
                main_output.write(self.external_style.getvalue())

        return Response(status=200, response=main_output.getvalue(), mimetype="text/css")
