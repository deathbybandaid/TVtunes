

class Startup_Tasks():
    endpoints = ["/api/startup_tasks"]
    endpoint_name = "api_startup_tasks"
    endpoint_methods = ["GET", "POST"]

    def __init__(self, tvtunes):
        self.tvtunes = tvtunes

        self.shows_update_url = "/api/tvshows?method=scanplex"
        self.shows_themescan_url = "/api/tvshows?method=scanfiles"

    def __call__(self, *args):
        return self.get(*args)

    def get(self, *args):

        self.tvtunes.logger.noob("Running Startup Tasks.")

        # Update Shows List from plex
        self.tvtunes.api.get(self.shows_update_url)

        # Scan Files
        self.tvtunes.api.get(self.shows_themescan_url)

        self.tvtunes.logger.noob("Startup Tasks Complete.")

        return "Success"
