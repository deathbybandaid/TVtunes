from flask import request, render_template, session


class TVShows_HTML():
    endpoints = ["/tvshows", "/tvshows.html"]
    endpoint_name = "page_tvshows_html"
    endpoint_access_level = 1
    endpoint_category = "tool_pages"
    pretty_name = "TV Shows"

    def __init__(self, tvtunes):
        self.tvtunes = tvtunes

    def __call__(self, *args):
        return self.get(*args)

    def get(self, *args):

        shows_info = {}

        for show_id in [x["id"] for x in self.tvtunes.tvshows.get_shows()]:
            show_obj = self.tvtunes.tvshows.list[show_id]
            if show_obj:
                show_dict = show_obj.dict.copy()
                show_dict["theme_file"] = show_obj.theme_file
                show_dict["theme_link"] = show_obj.plexcom_theme_url
                show_library = show_obj.library

                if show_library not in list(shows_info.keys()):
                    shows_info[show_library] = {}

                shows_info[show_library][show_obj.title] = show_dict

        libraries = list(shows_info.keys())

        if len(libraries):

            library = request.args.get('library', default=libraries[0], type=str)
            if library not in libraries:
                library = libraries[0]
        else:
            library = None

        return render_template('tvshows.html', request=request, session=session, tvtunes=self.tvtunes, shows_info=shows_info, libraries=libraries, library=library, list=list)
