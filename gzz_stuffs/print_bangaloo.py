import discord

from gzz_stuffs.util.EmoteEnum import Emote

current_patch = 1


def base_embed_and_load_bangaloo(bangaloo_id, bot):
    bangaloo = bot.bangaloos[bangaloo_id]

    embed = discord.Embed(
        title=bangaloo.name,
        description=f"{bangaloo.rarity_icon.value}{bangaloo.print_damage_types()}\n"
                    f"**Synergy:**\n"
                    f"{bangaloo.print_synergy()}"
    )

    if bangaloo.release_patch == 99:
        embed.set_footer(
            text="This entry is from skeleton data left on the game by MiHoYo, it doesn't mean "
                 "this is releasing soon, or at all, and all information is subject to changes before release."
        )

    elif bangaloo.release_patch > current_patch:
        embed.set_footer(
            text="This entry is from a future version, all information on it could be "
                 "inaccurate and is subject to changes before release."
        )

    embed.set_thumbnail(url=bangaloo.icon_image_url)
    # embed.colour = int(bangaloo.embed_color, 16)

    return bangaloo, embed


def print_bangaloo(bot, bangaloo_id="53001"):
    bangaloo, embed = base_embed_and_load_bangaloo(bangaloo_id, bot)

    embed.add_field(
        name=f"Stats at Lv1 → Lv60", inline=False,
        value=f"**{Emote.HP_STAT_ICON.value}HP:** {bangaloo.base_hp} → {bangaloo.hp_at_level(60)}\n"
              f"**{Emote.ATK_STAT_ICON.value}ATK:** {bangaloo.base_atk} → {bangaloo.atk_at_level(60)}\n"
              f"**{Emote.DEF_STAT_ICON.value}DEF:** {bangaloo.base_def} → {bangaloo.def_at_level(60)}\n"
              f"**{Emote.IMPACT_STAT_ICON.value}Impact:** {bangaloo.base_impact}\n"
              f"**{Emote.CRIT_RATE_STAT_ICON.value}CRIT Rate:** {bangaloo.print_crit_rate_at_level(0)} → {bangaloo.print_crit_rate_at_level(60)}\n"
              f"**{Emote.CRIT_DMG_STAT_ICON.value}CRIT DMG:** {bangaloo.print_crit_dmg_at_level(0)} → {bangaloo.print_crit_dmg_at_level(60)}\n"
              f"**{Emote.ANOMALY_MASTERY_STAT_ICON.value}Anomaly Mastery:** {bangaloo.base_anomaly_mastery}"
    )

    return embed


def print_bangaloo_at_level(bot, bangaloo_id="53001", level=60):
    bangaloo, embed = base_embed_and_load_bangaloo(bangaloo_id, bot)

    embed.add_field(
        name=f"Stats at Lv{level}", inline=False,
        value=f"**{Emote.HP_STAT_ICON.value}HP:** {bangaloo.hp_at_level(level)}\n"
              f"**{Emote.ATK_STAT_ICON.value}ATK:** {bangaloo.atk_at_level(level)}\n"
              f"**{Emote.DEF_STAT_ICON.value}DEF:** {bangaloo.def_at_level(level)}\n"
              f"**{Emote.IMPACT_STAT_ICON.value}Impact:** {bangaloo.base_impact}\n"
              f"**{Emote.CRIT_RATE_STAT_ICON.value}CRIT Rate:** {bangaloo.print_crit_rate_at_level(level)}\n"
              f"**{Emote.CRIT_DMG_STAT_ICON.value}CRIT DMG:** {bangaloo.print_crit_dmg_at_level(level)}\n"
              f"**{Emote.ANOMALY_MASTERY_STAT_ICON.value}Anomaly Mastery:** {bangaloo.base_anomaly_mastery}"
    )

    return embed
