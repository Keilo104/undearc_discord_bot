import math

from gzz_stuffs.util.EmoteEnum import Emote


def get_boost(level, boost_list):
    if level < 11:
        return boost_list[0]

    if level < 21:
        return boost_list[1]

    if level < 31:
        return boost_list[2]

    if level < 41:
        return boost_list[3]

    if level < 51:
        return boost_list[4]

    return boost_list[5]


class Bangaloo:
    rarity = "No data"
    rarity_icon = Emote.UNKNOWN_ICON
    damage_types = ["No data"]
    synergy = "No data"

    icon_image_url = "https://i.imgur.com/tmjMEtZ.png"

    def __init__(self, bangaloo_json, bangaloo_extra_infos_json):
        self.atk_boosts = [0, 0, 0, 0, 0]
        self.hp_boosts = [0, 0, 0, 0, 0]
        self.def_boosts = [0, 0, 0, 0, 0]

        self.crit_rate_boosts = [0, 0, 0, 0, 0, 0]
        self.crit_dmg_boosts = [0, 0, 0, 0, 0, 0]

        self.id = bangaloo_json["Id"]
        self.name = bangaloo_json["Name"]
        self.icon = Emote.get_icon_from_id(str(self.id))

        self.base_hp = bangaloo_json["Stats"]["HpMax"]
        self.hp_growth = bangaloo_json["Stats"]["Hpupgrade"]
        self.base_atk = bangaloo_json["Stats"]["Attack"]
        self.atk_growth = bangaloo_json["Stats"]["AttackUpgrade"]
        self.base_def = bangaloo_json["Stats"]["Defence"]
        self.def_growth = bangaloo_json["Stats"]["DefUpgrade"]

        self.base_impact = bangaloo_json["Stats"]["BreakStun"]
        self.base_anomaly_mastery = bangaloo_json["Stats"]["ElementAbnormalPower"]
        self.base_pen_ratio = bangaloo_json["Stats"]["PenRatio"]
        self.base_crit_rate = bangaloo_json["Stats"]["Crit"]
        self.base_crit_dmg = bangaloo_json["Stats"]["CritDmg"]

        if bangaloo_extra_infos_json[str(self.id)]["icon_image_url"] != "":
            self.icon_image_url = bangaloo_extra_infos_json[str(self.id)]["icon_image_url"]
        self.damage_types = bangaloo_extra_infos_json[str(self.id)]["damage_type"]
        self.synergy = bangaloo_extra_infos_json[str(self.id)]["synergy_type"]
        self.synergy_count = bangaloo_extra_infos_json[str(self.id)]["synergy_count"]
        self.release_patch = bangaloo_extra_infos_json[str(self.id)]["release_patch"]
        self.embed_color = bangaloo_extra_infos_json[str(self.id)]["embed_color"]

        if "override_name" in bangaloo_extra_infos_json[str(self.id)]:
            self.name = bangaloo_extra_infos_json[str(self.id)]["override_name"]

        self.figure_out_boosts(bangaloo_json)
        self.figure_out_rarity(bangaloo_json)
        self.figure_out_crit_boosts(bangaloo_json)

    def atk_at_level(self, level):
        return math.floor(self.base_atk + ((self.atk_growth * (level - 1)) / 10000) + self.atk_boost_at_level(level))

    def hp_at_level(self, level):
        return math.floor(self.base_hp + ((self.hp_growth * (level - 1)) / 10000) + self.hp_boost_at_level(level))

    def def_at_level(self, level):
        return math.floor(self.base_def + ((self.def_growth * (level - 1)) / 10000) + self.def_boost_at_level(level))

    def atk_boost_at_level(self, level):
        return get_boost(level, self.atk_boosts)

    def hp_boost_at_level(self, level):
        return get_boost(level, self.hp_boosts)

    def def_boost_at_level(self, level):
        return get_boost(level, self.def_boosts)

    def print_crit_rate_at_level(self, level):
        return f"{str(self.crit_rate_at_level(level) / 100).rstrip('0').rstrip('.')}%"

    def print_crit_dmg_at_level(self, level):
        return f"{str(self.crit_dmg_at_level(level) / 100).rstrip('0').rstrip('.')}%"

    def crit_rate_at_level(self, level):
        return self.base_crit_rate + get_boost(level, self.crit_rate_boosts)

    def crit_dmg_at_level(self, level):
        return self.base_crit_dmg + get_boost(level, self.crit_dmg_boosts)

    def print_damage_types(self):
        if self.damage_types is []:
            return Emote.UNKNOWN_ICON.value

        to_print = ""

        for damage_type in self.damage_types:
            if damage_type == "Ice":
                to_print = f"{to_print} {Emote.ICE_ICON.value}"
            elif damage_type == "Physical":
                to_print = f"{to_print} {Emote.PHYSICAL_ICON.value}"
            elif damage_type == "Ether":
                to_print = f"{to_print} {Emote.ETHER_ICON.value}"
            elif damage_type == "Fire":
                to_print = f"{to_print} {Emote.FIRE_ICON.value}"
            elif damage_type == "Electric":
                to_print = f"{to_print} {Emote.ELECTRIC_ICON.value}"
            elif damage_type == "HP Recovery":
                to_print = f"{to_print} {Emote.UNKNOWN_ICON.value}"
            elif damage_type == "Shield":
                to_print = f"{to_print} {Emote.UNKNOWN_ICON.value}"
            elif damage_type == "Energy Regen":
                to_print = f"{to_print} {Emote.UNKNOWN_ICON.value}"
            else:
                to_print = f"{to_print} {Emote.UNKNOWN_ICON.value}"

        return to_print

    def print_synergy(self):
        if self.synergy == "Ice":
            return f"{self.synergy_count}+ {Emote.ICE_ICON.value}Ice Attribute characters"
        if self.synergy == "Physical":
            return f"{self.synergy_count}+ {Emote.PHYSICAL_ICON.value}Physical Attribute characters"
        if self.synergy == "Ether":
            return f"{self.synergy_count}+ {Emote.ETHER_ICON.value}Ether Attribute characters"
        if self.synergy == "Fire":
            return f"{self.synergy_count}+ {Emote.FIRE_ICON.value}Fire Attribute characters"
        if self.synergy == "Electric":
            return f"{self.synergy_count}+ {Emote.ELECTRIC_ICON.value}Electric Attribute characters"
        if self.synergy == "Support":
            return f"{self.synergy_count}+ {Emote.SUPPORT_ICON.value}Support characters"
        if self.synergy == "Defense":
            return f"{self.synergy_count}+ {Emote.DEFENSE_ICON.value}Defense characters"
        if self.synergy == "Stun":
            return f"{self.synergy_count}+ {Emote.STUN_ICON.value}Stun characters"
        if self.synergy == "Attack":
            return f"{self.synergy_count}+ {Emote.ATTACK_ICON.value}Attack characters"
        if self.synergy == "Anomaly":
            return f"{self.synergy_count}+ {Emote.ANOMALY_ICON.value}Anomaly characters"
        if self.synergy == "Pierce":
            return f"{self.synergy_count}+ {Emote.PIERCE_ICON.value}Pierce-type characters"
        if self.synergy == "Strike":
            return f"{self.synergy_count}+ {Emote.STRIKE_ICON.value}Strike-type characters"
        if self.synergy == "Slash":
            return f"{self.synergy_count}+ {Emote.SLASH_ICON.value}Slash-type characters"
        if self.synergy == "Cunning Hares":
            return f"{self.synergy_count}+ characters from {Emote.CUNNING_HARES_ICON.value} Cunning Hares"
        if self.synergy == "Victoria Housekeeping Co.":
            return f"{self.synergy_count}+ characters from {Emote.VICTORIA_HOUSEKEEPING_ICON.value} Victoria Housekeeping Co."
        if self.synergy == "Belobog Heavy Industries":
            return f"{self.synergy_count}+ characters from {Emote.BELOBOG_INDUSTRIES_ICON.value} Belobog Heavy Industries"
        if self.synergy == "New Eridu Public Security":
            return f"{self.synergy_count}+ characters from {Emote.PUBLIC_SECURITY_ICON.value} New Eridu Public Security"

        return f"{Emote.UNKNOWN_ICON} No Data"

    def figure_out_boosts(self, bangaloo_json):
        if len(bangaloo_json["Level"].keys()) == 0:
            return

        self.hp_boosts = []
        self.atk_boosts = []
        self.def_boosts = []

        for level in bangaloo_json["Level"].keys():
            self.hp_boosts += [bangaloo_json["Level"][level]["HpMax"]]
            self.atk_boosts += [bangaloo_json["Level"][level]["Attack"]]
            self.def_boosts += [bangaloo_json["Level"][level]["Defence"]]

    def figure_out_rarity(self, bangaloo_json):
        if bangaloo_json["Rarity"] == 3:
            self.rarity = "A-Rank"
            self.rarity_icon = Emote.A_RANK_ICON

        elif bangaloo_json["Rarity"] == 4:
            self.rarity = "S-Rank"
            self.rarity_icon = Emote.S_RANK_ICON

    def figure_out_crit_boosts(self, bangaloo_json):
        if "1" not in bangaloo_json["Level"] or len(bangaloo_json["Level"]["1"]["Extra"].keys()) == 0:
            return

        stat_a, stat_b = "", ""
        self.crit_rate_boosts, self.crit_dmg_boosts = [], []

        for stat in bangaloo_json["Level"]["1"]["Extra"].keys():
            if bangaloo_json["Level"]["1"]["Extra"][stat]["Name"] == "CRIT Rate":
                stat_a = stat
            elif bangaloo_json["Level"]["1"]["Extra"][stat]["Name"] == "CRIT DMG":
                stat_b = stat

        for core_upgrade in bangaloo_json["Level"].keys():
            self.crit_rate_boosts += [bangaloo_json["Level"][core_upgrade]["Extra"][stat_a]["Value"]]
            self.crit_dmg_boosts += [bangaloo_json["Level"][core_upgrade]["Extra"][stat_b]["Value"]]
