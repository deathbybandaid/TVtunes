

from .plex_library import Plex_library


class TVtunes_Manager():
    """
    Methods for Managing Plex Libraries, Shows, and their Theme Music.
    """

    def __init__(self, tvtunes, plexinterface):
        self.tvtunes = tvtunes
        self.plexinterface = plexinterface

        self.get_db_libraries()

    def get_db_libraries(self):
        """
        Retrieve existing libraries from database.
        """

        self.tvtunes.logger.info("Checking for Library information stored in the database.")
        library_ids = self.tvtunes.db.get_tvtunes_value("libraries", "list") or []

        if len(library_ids):
            self.tvtunes.logger.info("Found %s existing libraries in the database." % str(len(library_ids)))

        for library_id in library_ids:
            library_ids_obj = Plex_library(self.tvtunes, self.plexinterface, library_id=library_id)
            library_id = library_ids_obj.dict["id"]
            self.list[library_id] = library_ids_obj
