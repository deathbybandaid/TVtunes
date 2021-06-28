import uuid


class Show_IDs():
    """
    TVtunes Show Identification system.
    """

    def __init__(self, tvtunes):
        self.tvtunes = tvtunes

    def get(self, plex_id, library):
        """
        Get a Channel ID for existing, or assign.
        """

        existing_ids = self.tvtunes.db.get_fhdhr_value("shows", "list", library) or []
        existing_channel_info = [self.tvtunes.db.get_fhdhr_value(show_id, "dict", library) or {} for show_id in existing_ids]
        for existing_channel in existing_channel_info:

            if existing_channel["plex_id"] == plex_id:
                return existing_channel["id"]

        return self.assign(library)

    def assign(self, origin):
        """
        Assign a channel an ID.
        """

        existing_ids = self.tvtunes.db.get_fhdhr_value("shows", "list", origin) or []

        show_id = None
        while not show_id:

            unique_id = str(uuid.uuid4())
            if str(unique_id) not in existing_ids:
                show_id = str(unique_id)

        existing_ids.append(show_id)
        self.tvtunes.db.set_fhdhr_value("shows", "list", existing_ids, origin)

        return show_id
