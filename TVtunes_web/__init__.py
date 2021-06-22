from gevent.pywsgi import WSGIServer
from flask import Flask, request, session
import threading
import uuid

from .pages import TVtunes_Pages
from .files import TVtunes_Files
from .brython import TVtunes_Brython
from .api import TVtunes_API


TVtunes_web_VERSION = "v0.9.0-beta"


class TVtunes_HTTP_Server():
    """
    TVtunes_web HTTP Frontend.
    """

    app = None

    def __init__(self, tvtunes):
        self.tvtunes = tvtunes

        self.template_folder = tvtunes.config.internal["paths"]["www_templates_dir"]

        self.tvtunes.logger.info("Loading Flask.")

        self.tvtunes.app = Flask("TVtunes", template_folder=self.template_folder)
        self.instance_id = str(uuid.uuid4())

        # Allow Internal API Usage
        self.tvtunes.app.testing = True
        self.tvtunes.api.client = self.tvtunes.app.test_client()

        # Set Secret Key For Sessions
        self.tvtunes.app.secret_key = self.tvtunes.config.dict["tvtunes"]["friendlyname"]

        self.route_list = {}

        self.endpoints_obj = {}
        self.endpoints_obj["brython"] = TVtunes_Brython(tvtunes)
        self.endpoints_obj["api"] = TVtunes_API(tvtunes)

        self.endpoints_obj["pages"] = TVtunes_Pages(tvtunes)
        self.endpoints_obj["files"] = TVtunes_Files(tvtunes)

        for endpoint_type in list(self.endpoints_obj.keys()):
            self.tvtunes.logger.info("Loading HTTP %s Endpoints." % endpoint_type)
            self.add_endpoints(endpoint_type)

        self.tvtunes.app.before_request(self.before_request)
        self.tvtunes.app.after_request(self.after_request)
        self.tvtunes.app.before_first_request(self.before_first_request)

        self.tvtunes.threads["flask"] = threading.Thread(target=self.run)

    def start(self):
        """
        Start Flask.
        """

        self.tvtunes.logger.info("Flask HTTP Thread Starting")
        self.tvtunes.threads["flask"].start()

    def stop(self):
        """
        Safely Stop Flask.
        """

        self.tvtunes.logger.info("Flask HTTP Thread Stopping")
        self.http.stop()

    def before_first_request(self):
        """
        Handling before a first request can be handled.
        """

        self.tvtunes.logger.info("HTTP Server Online.")

    def before_request(self):
        """
        Handling before a request is processed.
        """

        session["session_id"] = str(uuid.uuid4())
        session["instance_id"] = self.instance_id
        session["route_list"] = self.route_list

        session["user_agent"] = request.headers.get('User-Agent')

        session["is_internal_api"] = self.detect_internal_api(request)
        if session["is_internal_api"]:
            self.tvtunes.logger.debug("Client is using internal API call.")

        session["is_mobile"] = self.detect_mobile(request)
        if session["is_mobile"]:
            self.tvtunes.logger.debug("Client is a mobile device.")

        session["is_plexmediaserver"] = self.detect_plexmediaserver(request)
        if session["is_plexmediaserver"]:
            self.tvtunes.logger.debug("Client is a Plex Media Server.")

        session["deviceauth"] = self.detect_plexmediaserver(request)

        session["restart"] = False

        self.tvtunes.logger.debug("Client %s requested %s Opening" % (request.method, request.path))

    def after_request(self, response):
        """
        Handling after a request is processed.
        """

        self.tvtunes.logger.debug("Client %s requested %s Closing" % (request.method, request.path))

        if not session["restart"]:
            return response

        else:
            return self.stop()

    def detect_internal_api(self, request):
        """
        Detect if accessed by internal API.
        """

        user_agent = request.headers.get('User-Agent')
        if not user_agent:
            return False
        elif str(user_agent).lower().startswith("tvtunes"):
            return True
        else:
            return False

    def detect_deviceauth(self, request):
        """
        Detect if accessed with DeviceAuth.
        """

        return request.args.get('DeviceAuth', default=None, type=str)

    def detect_mobile(self, request):
        """
        Detect if accessed by mobile.
        """

        user_agent = request.headers.get('User-Agent')
        phones = ["iphone", "android", "blackberry"]

        if not user_agent:
            return False

        elif any(phone in user_agent.lower() for phone in phones):
            return True

        else:
            return False

    def detect_plexmediaserver(self, request):
        """
        Detect if accessed by plexmediaserver.
        """

        user_agent = request.headers.get('User-Agent')

        if not user_agent:
            return False

        elif str(user_agent).lower().startswith("plexmediaserver"):
            return True

        else:
            return False

    def add_endpoints(self, index_name):
        """
        Add Endpoints.
        """

        item_list = [x for x in dir(self.endpoints_obj[index_name]) if self.isapath(x)]
        endpoint_main = self.endpoints_obj[index_name]
        endpoint_main.tvtunes.version  # dummy line
        for item in item_list:
            endpoints = eval("endpoint_main.%s.%s" % (item, "endpoints"))
            if isinstance(endpoints, str):
                endpoints = [endpoints]
            handler = eval("endpoint_main.%s" % item)
            endpoint_name = eval("endpoint_main.%s.%s" % (item, "endpoint_name"))

            try:
                endpoint_methods = eval("endpoint_main.%s.%s" % (item, "endpoint_methods"))
            except AttributeError:
                endpoint_methods = ['GET']

            try:
                endpoint_access_level = eval("endpoint_main.%s.%s" % (item, "endpoint_access_level"))
            except AttributeError:
                endpoint_access_level = 0

            try:
                pretty_name = eval("endpoint_main.%s.%s" % (item, "pretty_name"))
            except AttributeError:
                pretty_name = endpoint_name

            try:
                endpoint_category = eval("endpoint_main.%s.%s" % (item, "endpoint_category"))
            except AttributeError:
                endpoint_category = index_name

            try:
                endpoint_default_parameters = eval("endpoint_main.%s.%s" % (item, "endpoint_default_parameters"))
            except AttributeError:
                endpoint_default_parameters = {}

            endpoint_added = True
            try:
                for endpoint in endpoints:
                    self.add_endpoint(endpoint=endpoint,
                                      endpoint_name=endpoint_name,
                                      handler=handler,
                                      methods=endpoint_methods)

            except AssertionError:
                endpoint_added = False

            if endpoint_added:
                self.tvtunes.logger.debug("Adding endpoint %s available at %s with %s methods." % (endpoint_name, ",".join(endpoints), ",".join(endpoint_methods)))

                if endpoint_category not in list(self.route_list.keys()):
                    self.route_list[endpoint_category] = {}

                if endpoint_name not in list(self.route_list[endpoint_category].keys()):
                    self.route_list[endpoint_category][endpoint_name] = {}

                self.route_list[endpoint_category][endpoint_name]["name"] = endpoint_name
                self.route_list[endpoint_category][endpoint_name]["endpoints"] = endpoints
                self.route_list[endpoint_category][endpoint_name]["endpoint_methods"] = endpoint_methods
                self.route_list[endpoint_category][endpoint_name]["endpoint_access_level"] = endpoint_access_level
                self.route_list[endpoint_category][endpoint_name]["endpoint_default_parameters"] = endpoint_default_parameters
                self.route_list[endpoint_category][endpoint_name]["pretty_name"] = pretty_name
                self.route_list[endpoint_category][endpoint_name]["endpoint_category"] = endpoint_category

    def isapath(self, item):
        """
        Ignore instances.
        """

        not_a_page_list = ["tvtunes"]
        if item in not_a_page_list:
            return False

        elif item.startswith("__") and item.endswith("__"):
            return False

        else:
            return True

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=['GET']):
        """
        Add Endpoint.
        """

        self.tvtunes.app.add_url_rule(endpoint, endpoint_name, handler, methods=methods)

    def run(self):
        """
        Run the WSGIServer.
        """

        self.http = WSGIServer(self.tvtunes.api.address_tuple,
                               self.tvtunes.app.wsgi_app,
                               log=self.tvtunes.logger.logger,
                               error_log=self.tvtunes.logger.logger)
        try:
            self.http.serve_forever()
            self.stop()
        except OSError as err:
            self.tvtunes.logger.error("HTTP Server Offline: %s" % err)
        except AttributeError:
            self.tvtunes.logger.info("HTTP Server Offline")
