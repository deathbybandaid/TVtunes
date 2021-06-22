from flask import request, render_template, session


class Index_HTML():
    endpoints = ["/index", "/index.html"]
    endpoint_name = "page_index_html"
    endpoint_access_level = 0
    pretty_name = "Index"

    def __init__(self, tvtunes):
        self.tvtunes = tvtunes

    def __call__(self, *args):
        return self.get(*args)

    def get(self, *args):

        tvtunes_status_dict = {
                            "Script Directory": str(self.tvtunes.config.internal["paths"]["script_dir"]),
                            "Config File": str(self.tvtunes.config.config_file),
                            "Cache Path": str(self.tvtunes.config.internal["paths"]["cache_dir"]),
                            "Database Type": self.tvtunes.config.dict["database"]["type"],
                            "Logging Level": self.tvtunes.config.dict["logging"]["level"],
                            }

        return render_template('index.html', request=request, session=session, tvtunes=self.tvtunes, tvtunes_status_dict=tvtunes_status_dict, list=list)
