import json

import discord

from gzz_stuffs.util.EmoteEnum import Emote
from gzz_stuffs.util.Valk import Valk

current_patch = 1


def base_embed_and_load_valk(valk_id):
    with open(f"gzz_stuffs/valks/{valk_id}.json", "r", encoding="utf-8") as valk_json_file:
        valk = Valk(json.load(valk_json_file))

    embed = discord.Embed(
        title=valk.name,
        description=f"{valk.faction_icon.value} • {valk.faction}\n"
        f"{valk.rarity_icon.value} {valk.element_icon.value} {valk.specialty_icon.value} {valk.damage_type_icon.value}"
    )

    if valk.release_patch > current_patch:
        embed.set_footer(
            text="This entry is from a future version, all information on it could be "
                 "inaccurate and is subject to changes before release."
        )

    embed.set_thumbnail(url=valk.icon_image_url)
    embed.colour = int(valk.embed_color, 16)

    return valk, embed


def print_valk(valk_id="1011"):
    valk, embed = base_embed_and_load_valk(valk_id)

    embed.add_field(
        inline=False, name="Base stats at Lv1 → Lv60",
        value=f"{Emote.HP_STAT_ICON.value} **HP:** {valk.base_hp} → {valk.hp_at_level(60)}\n"
              f"{Emote.ATK_STAT_ICON.value} **ATK:** {valk.base_atk} → {valk.atk_at_level(60)}\n"
              f"{Emote.DEF_STAT_ICON.value} **DEF:** {valk.base_def} → {valk.def_at_level(60)}\n"
              f"{f"{valk.print_core_first_stat()} {valk.print_first_core_stat_at_level(0)} → {valk.print_first_core_stat_at_level(60)}\n" if valk.has_first_stat() is True else ""}"
              f"{f"{valk.print_core_second_stat()} {valk.print_second_core_stat_at_level(0)} → {valk.print_second_core_stat_at_level(60)}\n" if valk.has_second_stat() is True else ""}"
              f"{Emote.IMPACT_STAT_ICON.value} **Impact:** {f"{valk.impact} → {valk.impact_at_level(60)}" if valk.scales_impact() else valk.impact}\n"
              f"{Emote.ANOMALY_MASTERY_STAT_ICON.value} **Anomaly Mastery:** {f"{valk.anomaly_mastery} → {valk.anomaly_mastery_at_level(60)}" if valk.scales_anomaly_mastery() else valk.anomaly_mastery}\n"
              f"{Emote.ANOMALY_PROFICIENCY_STAT_ICON.value} **Anomaly Proficiency:** {f"{valk.anomaly_proficiency} → {valk.anomaly_proficiency_at_level(60)}" if valk.scales_anomaly_proficiency() else valk.anomaly_proficiency}"
        )

    embed.add_field(
        inline=False, name=f"Core skill upgrade materials",
        value=f"{valk.print_purple_mat()}\n"
              f"{valk.print_golden_mat()}"
        )

    if valk.signature_weapon is not None:
        embed.add_field(
            name=f"", inline=False,
            value=f"{valk.name}'s signature weapon is **{valk.signature_weapon_icon} {valk.signature_weapon}**"
        )

    return embed


def print_valk_at_level(valk_id="1011", level=60):
    valk, embed = base_embed_and_load_valk(valk_id)

    embed.add_field(
        inline=False, name=f"Base stats at Lv{level}",
        value=f"{Emote.HP_STAT_ICON.value} **HP:** {valk.hp_at_level(level)}\n"
              f"{Emote.ATK_STAT_ICON.value} **ATK:** {valk.atk_at_level(level)}\n"
              f"{Emote.DEF_STAT_ICON.value} **DEF:** {valk.def_at_level(level)}\n"
              f"{f"{valk.print_core_first_stat()} {valk.print_first_core_stat_at_level(level)}\n" if valk.has_first_stat() is True else ""}"
              f"{f"{valk.print_core_second_stat()} {valk.print_second_core_stat_at_level(level)}\n" if valk.has_second_stat() is True else ""}"
              f"{Emote.IMPACT_STAT_ICON.value} **Impact:** {valk.impact_at_level(level)}\n"
              f"{Emote.ANOMALY_MASTERY_STAT_ICON.value} **Anomaly Mastery:** {valk.anomaly_mastery_at_level(level)}\n"
              f"{Emote.ANOMALY_PROFICIENCY_STAT_ICON.value} **Anomaly Proficiency:** {valk.anomaly_proficiency_at_level(level)}"
        )

    return embed
