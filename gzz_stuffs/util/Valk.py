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


def core_stat_at_level(level, core_list):
    if level < 15:
        return 0

    if level < 25:
        return core_list[0]

    if level < 35:
        return core_list[1]

    if level < 45:
        return core_list[2]

    if level < 55:
        return core_list[3]

    if level < 60:
        return core_list[4]

    return core_list[5]


def print_core_stat(core_stat):
    if core_stat == "Base Energy Regen":
        return f"{Emote.ENERGY_REGEN_STAT_ICON.value}  **Energy Regen:**"

    if core_stat == "CRIT Rate":
        return f"{Emote.CRIT_RATE_STAT_ICON.value}  **CRIT Rate:**"

    if core_stat == "CRIT DMG":
        return f"{Emote.CRIT_DMG_STAT_ICON.value} **CRIT DMG:**"

    if core_stat == "PEN Ratio":
        return f"{Emote.PEN_RATIO_STAT_ICON.value} **PEN Ratio:**"


class Valk:
    damage_type = "No data"
    damage_type_icon = Emote.UNKNOWN_ICON
    specialty = "No data"
    specialty_icon = Emote.UNKNOWN_ICON
    element = "No data"
    element_icon = Emote.UNKNOWN_ICON
    faction = "No data"
    faction_icon = Emote.UNKNOWN_ICON
    rarity = "No data"
    rarity_icon = Emote.UNKNOWN_ICON

    icon_image_url = "https://i.imgur.com/lQlL7DG.png"

    core_first_stat = None
    core_second_stat = None
    purple_mat = None
    golden_mat = None

    signature_weapon = None

    def __init__(self, valk_json, valk_extra_infos_json):
        self.hp_boosts = [0, 0, 0, 0, 0, 0]
        self.atk_boosts = [0, 0, 0, 0, 0, 0]
        self.def_boosts = [0, 0, 0, 0, 0, 0]

        self.core_first_stat_values = [0, 0, 0, 0, 0, 0]
        self.core_second_stat_values = [0, 0, 0, 0, 0, 0]

        self.id = valk_json["Id"]
        self.icon = Emote.get_icon_from_id(str(self.id))
        self.name = valk_json["Name"]
        self.full_name = valk_json["PartnerInfo"]["FullName"] if "FullName" in valk_json["PartnerInfo"] else None

        self.base_hp = valk_json["Stats"]["HpMax"] if "HpMax" in valk_json["Stats"] else 0
        self.hp_growth = valk_json["Stats"]["HpGrowth"] if "HpGrowth" in valk_json["Stats"] else 0
        self.base_atk = valk_json["Stats"]["Attack"] if "Attack" in valk_json["Stats"] else 0
        self.atk_growth = valk_json["Stats"]["AttackGrowth"] if "AttackGrowth" in valk_json["Stats"] else 0
        self.base_def = valk_json["Stats"]["Defence"] if "Defence" in valk_json["Stats"] else 0
        self.def_growth = valk_json["Stats"]["DefenceGrowth"] if "DefenceGrowth" in valk_json["Stats"] else 0
        self.impact = valk_json["Stats"]["BreakStun"] if "BreakStun" in valk_json["Stats"] else 0
        self.anomaly_mastery = valk_json["Stats"]["ElementMystery"] if "ElementMystery" in valk_json["Stats"] else 0
        self.anomaly_proficiency = valk_json["Stats"]["ElementAbnormalPower"] if "ElementAbnormalPower" in valk_json["Stats"] else 0

        self.name = valk_extra_infos_json[str(self.id)]["override_name"] if "override_name" in valk_extra_infos_json[str(self.id)] else self.name
        self.full_name = valk_extra_infos_json[str(self.id)]["override_full_name"] if "override_full_name" in valk_extra_infos_json[str(self.id)] else self.full_name

        if valk_extra_infos_json[str(self.id)]["icon_image_url"] != "":
            self.icon_image_url = valk_extra_infos_json[str(self.id)]["icon_image_url"]

        if "signature_weapon" in valk_extra_infos_json[str(self.id)]:
            self.signature_weapon = valk_extra_infos_json[str(self.id)]["signature_weapon"]

        self.release_patch = valk_extra_infos_json[str(self.id)]["release_patch"]
        self.embed_color = valk_extra_infos_json[str(self.id)]["embed_color"]

        self.figure_out_rarity(valk_json)
        self.figure_out_faction(valk_json)
        self.figure_out_element(valk_json)
        self.figure_out_specialty(valk_json)
        self.figure_out_damage_type(valk_json)

        self.figure_out_core_stats(valk_json)
        self.figure_out_boosts(valk_json)
        self.figure_out_talent_mats(valk_json)

    def hp_at_level(self, level):
        if self.core_first_stat == "":
            return math.floor(self.base_hp + ((self.hp_growth * (level - 1)) / 10000) + self.hp_boost_at_level(level) +
                              self.first_core_stat_at_level(level))

        elif self.core_second_stat == "":
            return math.floor(self.base_hp + ((self.hp_growth * (level - 1)) / 10000) + self.hp_boost_at_level(level) +
                              self.second_core_stat_at_level(level))

        else:
            return math.floor(self.base_hp + ((self.hp_growth * (level - 1)) / 10000) + self.hp_boost_at_level(level))

    def atk_at_level(self, level):
        if self.core_first_stat == "Base ATK":
            return math.floor(self.base_atk + ((self.atk_growth * (level - 1)) / 10000) + self.atk_boost_at_level(level) +
                              self.first_core_stat_at_level(level))

        elif self.core_second_stat == "Base ATK":
            return math.floor(self.base_atk + ((self.atk_growth * (level - 1)) / 10000) + self.atk_boost_at_level(level) +
                              self.second_core_stat_at_level(level))

        else:
            return math.floor(self.base_atk + ((self.atk_growth * (level - 1)) / 10000) + self.atk_boost_at_level(level))

    def def_at_level(self, level):
        if self.core_first_stat == "":
            return math.floor(self.base_def + ((self.def_growth * (level - 1)) / 10000) + self.def_boost_at_level(level) +
                              self.first_core_stat_at_level(level))

        elif self.core_second_stat == "":
            return math.floor(self.base_def + ((self.def_growth * (level - 1)) / 10000) + self.def_boost_at_level(level) +
                              self.second_core_stat_at_level(level))

        else:
            return math.floor(self.base_def + ((self.def_growth * (level - 1)) / 10000) + self.def_boost_at_level(level))

    def impact_at_level(self, level):
        if self.core_first_stat == "Impact":
            return self.impact + self.first_core_stat_at_level(level)

        elif self.core_second_stat == "Impact":
            return self.impact + self.second_core_stat_at_level(level)

        else:
            return self.impact

    def anomaly_mastery_at_level(self, level):
        if self.core_first_stat == "Anomaly Mastery":
            return self.anomaly_mastery + self.first_core_stat_at_level(level)

        elif self.core_second_stat == "Anomaly Mastery":
            return self.anomaly_mastery + self.second_core_stat_at_level(level)

        else:
            return self.anomaly_mastery

    def anomaly_proficiency_at_level(self, level):
        if self.core_first_stat == "":
            return self.anomaly_proficiency + self.first_core_stat_at_level(level)

        elif self.core_second_stat == "":
            return self.anomaly_proficiency + self.second_core_stat_at_level(level)

        else:
            return self.anomaly_proficiency

    def first_core_stat_at_level(self, level):
        return core_stat_at_level(level, self.core_first_stat_values)

    def second_core_stat_at_level(self, level):
        return core_stat_at_level(level, self.core_second_stat_values)

    def print_first_core_stat_at_level(self, level):
        if self.core_first_stat == "Base Energy Regen":
            return f"{str(1.2 + (self.first_core_stat_at_level(level) / 100)).rstrip('0').rstrip('.')}/s"

        if self.core_first_stat == "CRIT Rate":
            return f"{str(5 + (self.first_core_stat_at_level(level) / 100)).rstrip('0').rstrip('.')}%"

        if self.core_first_stat == "CRIT DMG":
            return f"{str(50 + (self.first_core_stat_at_level(level) / 100)).rstrip('0').rstrip('.')}%"

        if self.core_first_stat == "PEN Ratio":
            return f"{str(self.first_core_stat_at_level(level) / 100).rstrip('0').rstrip('.')}%"

    def print_second_core_stat_at_level(self, level):
        if self.core_second_stat == "Base Energy Regen":
            return f"{str(1.2 + (self.second_core_stat_at_level(level) / 100)).rstrip('0').rstrip('.')}/s"

        if self.core_second_stat == "CRIT Rate":
            return f"{str(5 + (self.second_core_stat_at_level(level) / 100)).rstrip('0').rstrip('.')}%"

        if self.core_second_stat == "CRIT DMG":
            return f"{str(50 + (self.second_core_stat_at_level(level) / 100)).rstrip('0').rstrip('.')}%"

        if self.core_second_stat == "PEN Ratio":
            return f"{str(self.second_core_stat_at_level(level) / 100).rstrip('0').rstrip('.')}%"

    def print_core_first_stat(self):
        return print_core_stat(self.core_first_stat)

    def print_core_second_stat(self):
        return print_core_stat(self.core_second_stat)

    def print_purple_mat(self):
        if self.purple_mat is None:
            return f"{Emote.UNKNOWN_ICON.value} No Data"

        if self.purple_mat == "110501":
            return f"{Emote.MINIBOSS1_MAT_ICON.value} Murderous Obituary"

        if self.purple_mat == "110502":
            return f"{Emote.MINIBOSS2_MAT_ICON.value} Crimson Awe"

        if self.purple_mat == "110503":
            return f"{Emote.MINIBOSS3_MAT_ICON.value} Ethereal Pursuit"

        if self.purple_mat == "110504":
            return f"{Emote.MINIBOSS4_MAT_ICON.value} Steel Malice"

        if self.purple_mat == "110505":
            return f"{Emote.MINIBOSS5_MAT_ICON.value} Destructive Advance"

        if self.purple_mat == "110506":
            return f"{Emote.MINIBOSS6_MAT_ICON.value} 1.1 New Material"

    def print_golden_mat(self):
        if self.golden_mat is None:
            return f"{Emote.UNKNOWN_ICON.value} No Data"

        if self.golden_mat == "110001":
            return f"{Emote.BOSS1_MAT_ICON.value} Ferocious Grip"

        if self.golden_mat == "110002":
            return f"{Emote.BOSS2_MAT_ICON.value} Living Drive"

        if self.golden_mat == "110003":
            return f"{Emote.BOSS3_MAT_ICON.value} Finale Dance Shoes"

    def scales_impact(self):
        return (self.core_first_stat == "Impact") or (self.core_second_stat == "Impact")

    def scales_anomaly_mastery(self):
        return (self.core_first_stat == "Anomaly Mastery") or (self.core_second_stat == "Anomaly Mastery")

    def scales_anomaly_proficiency(self):
        return (self.core_first_stat == "") or (self.core_second_stat == "")

    def has_first_stat(self):
        return self.core_first_stat not in [None, "", "Base ATK", "", "Impact", "Anomaly Mastery", ""]

    def has_second_stat(self):
        return self.core_second_stat not in [None, "", "Base ATK", "", "Impact", "Anomaly Mastery", ""]

    def hp_boost_at_level(self, level):
        return get_boost(level, self.hp_boosts)

    def atk_boost_at_level(self, level):
        return get_boost(level, self.atk_boosts)

    def def_boost_at_level(self, level):
        return get_boost(level, self.def_boosts)

    def figure_out_talent_mats(self, valk_json):
        if "Materials" not in valk_json["Passive"]:
            return

        for material in valk_json["Passive"]["Materials"]["6"].keys():
            if valk_json["Passive"]["Materials"]["6"][material] == 30:
                self.purple_mat = material

            elif valk_json["Passive"]["Materials"]["6"][material] == 4:
                self.golden_mat = material

    def figure_out_boosts(self, valk_json):
        if len(valk_json["Level"].keys()) == 0:
            return

        self.hp_boosts = []
        self.atk_boosts = []
        self.def_boosts = []

        for level in valk_json["Level"].keys():
            self.hp_boosts += [valk_json["Level"][level]["HpMax"]]
            self.atk_boosts += [valk_json["Level"][level]["Attack"]]
            self.def_boosts += [valk_json["Level"][level]["Defence"]]

    def figure_out_core_stats(self, valk_json):
        stat_a, stat_b = "", ""

        if "1" not in valk_json["ExtraLevel"]:
            return

        for stat in valk_json["ExtraLevel"]["1"]["Extra"].keys():
            if stat_a == "":
                stat_a = stat
                self.core_first_stat = valk_json["ExtraLevel"]["1"]["Extra"][stat]["Name"]

            else:
                stat_b = stat
                self.core_second_stat = valk_json["ExtraLevel"]["1"]["Extra"][stat]["Name"]

        if valk_json["ExtraLevel"]["1"]["Extra"][stat_a]["Value"] != 0:
            stat_a, stat_b = stat_b, stat_a
            self.core_first_stat, self.core_second_stat = self.core_second_stat, self.core_first_stat

        for core_upgrade in valk_json["ExtraLevel"].keys():
            self.core_first_stat_values += [valk_json["ExtraLevel"][core_upgrade]["Extra"][stat_a]["Value"]]
            self.core_second_stat_values += [valk_json["ExtraLevel"][core_upgrade]["Extra"][stat_b]["Value"]]

    def figure_out_rarity(self, valk_json):
        if valk_json["Rarity"] == 3:
            self.rarity = "A-Rank"
            self.rarity_icon = Emote.A_RANK_ICON

        elif valk_json["Rarity"] == 4:
            self.rarity = "S-Rank"
            self.rarity_icon = Emote.S_RANK_ICON

    def figure_out_faction(self, valk_json):
        if "1" in valk_json["Camp"]:
            self.faction = "Cunning Hares"
            self.faction_icon = Emote.CUNNING_HARES_ICON

        elif "2" in valk_json["Camp"]:
            self.faction = "Victoria Housekeeping Co."
            self.faction_icon = Emote.VICTORIA_HOUSEKEEPING_ICON

        elif "3" in valk_json["Camp"]:
            self.faction = "Belobog Heavy Industries"
            self.faction_icon = Emote.BELOBOG_INDUSTRIES_ICON

        elif "4" in valk_json["Camp"]:
            self.faction = "Sons of Calydon"
            self.faction_icon = Emote.SONS_OF_CALYDON_ICON

        elif "5" in valk_json["Camp"]:
            self.faction = "Obol Squad"
            self.faction_icon = Emote.OBOLS_ICON

        elif "6" in valk_json["Camp"]:
            self.faction = "Hollow Special Operations Section 6"
            self.faction_icon = Emote.HSOS6_ICON

        elif "7" in valk_json["Camp"]:
            self.faction = "New Eridu Public Security"
            self.faction_icon = Emote.PUBLIC_SECURITY_ICON

    def figure_out_element(self, valk_json):
        if "200" in valk_json["ElementType"]:
            self.element = "Physical"
            self.element_icon = Emote.PHYSICAL_ICON

        elif "201" in valk_json["ElementType"]:
            self.element = "Fire"
            self.element_icon = Emote.FIRE_ICON

        elif "202" in valk_json["ElementType"]:
            self.element = "Ice"
            self.element_icon = Emote.ICE_ICON

        elif "203" in valk_json["ElementType"]:
            self.element = "Electric"
            self.element_icon = Emote.ELECTRIC_ICON

        elif "205" in valk_json["ElementType"]:
            self.element = "Ether"
            self.element_icon = Emote.ETHER_ICON

    def figure_out_specialty(self, valk_json):
        if "1" in valk_json["WeaponType"]:
            self.specialty = "Attack"
            self.specialty_icon = Emote.ATTACK_ICON

        elif "2" in valk_json["WeaponType"]:
            self.specialty = "Stun"
            self.specialty_icon = Emote.STUN_ICON

        elif "3" in valk_json["WeaponType"]:
            self.specialty = "Anomaly"
            self.specialty_icon = Emote.ANOMALY_ICON

        elif "4" in valk_json["WeaponType"]:
            self.specialty = "Support"
            self.specialty_icon = Emote.SUPPORT_ICON

        elif "5" in valk_json["WeaponType"]:
            self.specialty = "Defense"
            self.specialty_icon = Emote.DEFENSE_ICON

    def figure_out_damage_type(self, valk_json):
        if "101" in valk_json["HitType"]:
            self.damage_type = "Slash"
            self.damage_type_icon = Emote.SLASH_ICON

        elif "102" in valk_json["HitType"]:
            self.damage_type = "Strike"
            self.damage_type_icon = Emote.STRIKE_ICON

        elif "103" in valk_json["HitType"]:
            self.damage_type = "Pierce"
            self.damage_type_icon = Emote.PIERCE_ICON
