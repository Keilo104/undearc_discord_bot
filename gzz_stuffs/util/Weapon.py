import json
import math

from gzz_stuffs.util.EmoteEnum import Emote


def prettify_description(description):
    return (
        description
        .replace("Special Attack", f"{Emote.SKILL_ICON.value}Special Attack")
        .replace(f"EX {Emote.SKILL_ICON.value}Special Attack", f"{Emote.SKILL_FILLED_ICON.value}EX Special Attack")
        .replace("Basic Attack", f"{Emote.BASIC_ATTACK_ICON.value}Basic Attack")
        .replace("Dash Attack", f"{Emote.DODGE_ICON.value}Dash Attack")
        .replace("Dodge Counter", f"{Emote.DODGE_ICON.value}Dodge Counter")
        .replace("Chain Attack", f"{Emote.ULTIMATE_ICON.value}Chain Attack")
        .replace("Assist Attack", f"{Emote.QUICK_ASSIST_ICON.value}Assist Attack")
        .replace("Quick Assist", f"{Emote.QUICK_ASSIST_ICON.value}Quick Assist")
        .replace("Ultimate", f"{Emote.ULTIMATE_FILLED_ICON.value}Ultimate")
        .replace("HP", f"{Emote.HP_STAT_ICON.value}HP")
        .replace(f"Max {Emote.HP_STAT_ICON.value}HP", f"{Emote.HP_STAT_ICON.value}Max HP")
        .replace("ATK", f"{Emote.ATK_STAT_ICON.value}ATK")
        .replace("DEF", f"{Emote.DEF_STAT_ICON.value}DEF")
        .replace("Impact", f"{Emote.IMPACT_STAT_ICON.value}Impact")
        .replace("Energy Regen", f"{Emote.ENERGY_REGEN_STAT_ICON.value}Energy Regen")
        .replace("Energy Generation Rate", f"{Emote.ENERGY_GENERATION_RATE_STAT_ICON.value}Energy Generation Rate")
        .replace("Anomaly Mastery", f"{Emote.ANOMALY_MASTERY_STAT_ICON.value}Anomaly Mastery")
        .replace("Anomaly Proficiency", f"{Emote.ANOMALY_PROFICIENCY_STAT_ICON.value}Anomaly Proficiency")
        .replace("CRIT Rate", f"{Emote.CRIT_RATE_STAT_ICON.value}CRIT Rate")
        .replace("<color=#2eb6ff>", f"{Emote.ELECTRIC_ICON.value}")
        .replace("<color=#fe437e>", f"{Emote.ETHER_ICON.value}")
        .replace("<color=#f0d12b>", f"{Emote.PHYSICAL_ICON.value}")
        .replace("<color=#98eff0>", f"{Emote.ICE_ICON.value}")
        .replace("<color=#ffffff>", "")
        .replace("<color=#2BAD00>", "")
        .replace("</color>", "")
        .replace("`", "\\`")
    )


class Weapon:
    rarity = None
    rarity_icon = None

    type = None
    type_icon = None

    def __init__(self, weapon_json):
        self.substat_scaling = []
        self.mainstat_scaling = []
        self.mainstat_boost_scaling = []
        self.effect_tiers = []

        self.id = weapon_json["Id"]
        self.name = weapon_json["Name"]
        self.main_stat = weapon_json["BaseProperty"]["Name"]
        self.main_stat_base = weapon_json["BaseProperty"]["Value"]

        self.substat = weapon_json["RandProperty"]["Name"]
        self.substat_base = weapon_json["RandProperty"]["Value"]

        for key in weapon_json["Stars"]:
            self.mainstat_boost_scaling += [weapon_json["Stars"][key]["StarRate"]]
            self.substat_scaling += [weapon_json["Stars"][key]["RandRate"]]

        for key in weapon_json["Level"]:
            self.mainstat_scaling += [weapon_json["Level"][key]["Rate"]]

        self.figure_out_rarity(weapon_json)
        self.figure_out_type(weapon_json)

        self.effect_name = weapon_json["Talents"]["1"]["Name"]
        for key in weapon_json["Talents"]:
            self.effect_tiers += [weapon_json["Talents"][key]["Desc"]]

        self.true_description = self.generate_true_description()

        with open("gzz_stuffs/util/weapon_extra_infos.json", "r", encoding="utf-8") as weapon_extra_infos_json_file:
            weapon_extra_infos_json = json.load(weapon_extra_infos_json_file)

        self.icon_image_url = weapon_extra_infos_json[str(self.id)]["icon_image_url"]
        self.obtain = weapon_extra_infos_json[str(self.id)]["obtain"] if "obtain" in weapon_extra_infos_json[str(self.id)] else "Craftable"
        self.signature = weapon_extra_infos_json[str(self.id)]["signature"] if "signature" in weapon_extra_infos_json[str(self.id)] else None
        self.signature_icon = weapon_extra_infos_json[str(self.id)]["signature_icon"] if "signature_icon" in weapon_extra_infos_json[str(self.id)] else None
        self.embed_color = weapon_extra_infos_json[str(self.id)]["embed_color"] if "embed_color" in weapon_extra_infos_json[str(self.id)] else "0x000000"
        self.release_patch = weapon_extra_infos_json[str(self.id)]["release_patch"] if "release_patch" in weapon_extra_infos_json[str(self.id)] else 1
        self.name = weapon_extra_infos_json[str(self.id)]["override_name"] if "override_name" in weapon_extra_infos_json[str(self.id)] else self.name
        self.effect_name = weapon_extra_infos_json[str(self.id)]["override_description_name"] if "override_description_name" in weapon_extra_infos_json[str(self.id)] else self.effect_name
        self.true_description = prettify_description(weapon_extra_infos_json[str(self.id)]["override_description"]) if "override_description" in weapon_extra_infos_json[str(self.id)] else self.true_description

    def generate_true_description(self):
        true_description = ""
        description_1 = prettify_description(self.effect_tiers[0]).split()
        description_2 = prettify_description(self.effect_tiers[1]).split()
        description_3 = prettify_description(self.effect_tiers[2]).split()
        description_4 = prettify_description(self.effect_tiers[3]).split()
        description_5 = prettify_description(self.effect_tiers[4]).split()

        for x in range(len(description_1)):
            if description_1[x] != description_2[x]:
                extras = ""
                for item in [",", ".", "%", "/s", "s"]:
                    if description_1[x].endswith(item):
                        extras = f"{item}{extras}"
                        description_1[x] = description_1[x][:-len(item)]
                        description_2[x] = description_2[x][:-len(item)]
                        description_3[x] = description_3[x][:-len(item)]
                        description_4[x] = description_4[x][:-len(item)]
                        description_5[x] = description_5[x][:-len(item)]

                true_description = f"{true_description} **{description_1[x]}/{description_2[x]}/{description_3[x]}/{description_4[x]}/{description_5[x]}{extras}**"
            else:
                true_description = f"{true_description} {description_1[x]}"

        return true_description

    def get_obtain_icon(self):
        if self.obtain == "Craftable":
            return Emote.WEAPON_CRAFTABLE_ICON.value
        if self.obtain == "Battlepass":
            return Emote.WEAPON_BATTLEPASS_ICON.value
        if self.obtain == "Gacha":
            return Emote.WEAPON_GACHA_ICON.value
        if self.obtain == "Event":
            return f" • Obtained in an event"

    def get_mainstat_at_level(self, level):
        return f"{math.floor(
            self.main_stat_base * (1 + ((self.mainstat_scaling[level] + self.mainstat_boost_at_level(level)) / 10000))
        )}".rstrip('0').rstrip('.')

    def mainstat_boost_at_level(self, level):
        if level < 11:
            return self.mainstat_boost_scaling[0]

        if level < 21:
            return self.mainstat_boost_scaling[1]

        if level < 31:
            return self.mainstat_boost_scaling[2]

        if level < 41:
            return self.mainstat_boost_scaling[3]

        if level < 51:
            return self.mainstat_boost_scaling[4]

        return self.mainstat_boost_scaling[5]

    def figure_out_rarity(self, weapon_json):
        if weapon_json["Rarity"] == 2:
            self.rarity = "B-rank"
            self.rarity_icon = Emote.GEAR_B_RANK_ICON
        elif weapon_json["Rarity"] == 3:
            self.rarity = "A-rank"
            self.rarity_icon = Emote.GEAR_A_RANK_ICON
        elif weapon_json["Rarity"] == 4:
            self.rarity = "S-rank"
            self.rarity_icon = Emote.GEAR_S_RANK_ICON

    def figure_out_type(self, weapon_json):
        if "1" in weapon_json["WeaponType"]:
            self.type = "Attack"
            self.type_icon = Emote.ATTACK_ICON
        elif "2" in weapon_json["WeaponType"]:
            self.type = "Stun"
            self.type_icon = Emote.STUN_ICON
        elif "3" in weapon_json["WeaponType"]:
            self.type = "Anomaly"
            self.type_icon = Emote.ANOMALY_ICON
        elif "4" in weapon_json["WeaponType"]:
            self.type = "Support"
            self.type_icon = Emote.SUPPORT_ICON
        elif "5" in weapon_json["WeaponType"]:
            self.type = "Defense"
            self.type_icon = Emote.DEFENSE_ICON

    def get_substat_scaling_at_level(self, level):
        if level < 11:
            return self.substat_scaling[0]

        if level < 21:
            return self.substat_scaling[1]

        if level < 31:
            return self.substat_scaling[2]

        if level < 41:
            return self.substat_scaling[3]

        if level < 51:
            return self.substat_scaling[4]

        return self.substat_scaling[5]

    def print_mainstat(self):
        if self.main_stat == "Base ATK":
            return  f"**{Emote.ATK_STAT_ICON.value} Base ATK:**"

    def print_substat(self):
        if self.substat == "Anomaly Proficiency":
            return f"**{Emote.ANOMALY_PROFICIENCY_STAT_ICON.value} Anomaly Proficiency:**"
        if self.substat == "Impact":
            return f"**{Emote.IMPACT_STAT_ICON.value} Impact:**"
        if self.substat == "CRIT DMG":
            return f"**{Emote.CRIT_DMG_STAT_ICON.value} CRIT DMG:**"
        if self.substat == "PEN Ratio":
            return f"**{Emote.PEN_RATIO_STAT_ICON.value} PEN Ratio:**"
        if self.substat == "Crit Rate":
            return f"**{Emote.CRIT_RATE_STAT_ICON.value} Crit Rate:**"
        if self.substat == "ATK":
            return f"**{Emote.ATK_STAT_ICON.value} ATK:**"
        if self.substat == "Energy Regen":
            return f"**{Emote.ENERGY_REGEN_STAT_ICON.value} Energy Regen:**"
        if self.substat == "DEF":
            return f"**{Emote.DEF_STAT_ICON.value} DEF:**"
        if self.substat == "HP":
            return f"**{Emote.HP_STAT_ICON.value} HP:**"

    def print_substat_at_level(self, level):
        if self.substat == "Anomaly Proficiency":
            return f"{self.substat_base * (1 + (self.get_substat_scaling_at_level(level) / 10000))}".rstrip('0').rstrip('.')

        else:
            return f"{f"{(self.substat_base * (1 + (self.get_substat_scaling_at_level(level) / 10000))) / 100}".rstrip('0').rstrip('.')}%"
