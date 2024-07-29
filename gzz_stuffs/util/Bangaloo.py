from gzz_stuffs.util.EmoteEnum import Emote


class Bangaloo:
    rarity = "No data"
    rarity_icon = Emote.UNKNOWN_ICON

    def __init__(self, bangaloo_json, bangaloo_extra_infos_json):
        self.id = bangaloo_json["Id"]
        self.name = bangaloo_json["Name"]
        self.icon = Emote.get_icon_from_id(str(self.id))


