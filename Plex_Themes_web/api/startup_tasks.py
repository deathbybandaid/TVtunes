

class Startup_Tasks():
    endpoints = ["/api/startup_tasks"]
    endpoint_name = "api_startup_tasks"
    endpoint_methods = ["GET", "POST"]

    def __init__(self, tvtunes):
        self.tvtunes = tvtunes

    def __call__(self, *args):
        return self.get(*args)

    def get(self, *args):

        self.tvtunes.logger.noob("Running Startup Tasks.")

        self.tvtunes.logger.noob("Startup Tasks Complete.")

        return "Success"
