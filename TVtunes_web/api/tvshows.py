from flask import request, redirect, Response
import urllib.parse
import json


class TVShows():
    endpoints = ["/api/tvshows"]
    endpoint_name = "api_tvshows"
    endpoint_methods = ["GET", "POST"]

    def __init__(self, tvtunes):
        self.tvtunes = tvtunes

    def __call__(self, *args):
        return self.get(*args)

    def get(self, *args):

        method = request.args.get('method', default="get", type=str)
        redirect_url = request.args.get('redirect', default=None, type=str)

        if method == "get":

            shows_info = {}

            for show_id in [x["id"] for x in self.tvtunes.tvshows.get_shows()]:
                show_obj = self.tvtunes.tvshows.list[show_id]
                if show_obj:
                    show_dict = show_obj.dict.copy()
                    shows_info[show_obj.title] = show_dict

            show_info_json = json.dumps(shows_info, indent=4)

            return Response(status=200,
                            response=show_info_json,
                            mimetype='application/json')

        elif method == "scan":
            self.tvtunes.tvshows.get_shows(forceupdate=True)

        if redirect_url:
            if "?" in redirect_url:
                return redirect("%s&retmessage=%s" % (redirect_url, urllib.parse.quote("%s Success" % method)))
            else:
                return redirect("%s?retmessage=%s" % (redirect_url, urllib.parse.quote("%s Success" % method)))
        else:
            return "%s Success" % method
