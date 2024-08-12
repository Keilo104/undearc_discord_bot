import discord


def base_embed_and_load_weapon(weapon_id, bot):
    weapon = bot.weapons[weapon_id]

    embed = discord.Embed(
        title=weapon.name,
        description=f"{weapon.rarity_icon.value} {weapon.type_icon.value} {weapon.get_obtain_icon()}"
    )

    if weapon.release_patch == 99:
        embed.set_footer(
            text="This entry is from skeleton data left on the game by MiHoYo, it doesn't mean "
                 "this is releasing soon, or at all, and all information is subject to changes before release."
        )

    elif weapon.release_patch > bot.current_patch:
        embed.set_footer(
            text="This entry is from a future version, all information on it could be "
                 "inaccurate and is subject to changes before release."
        )

    embed.add_field(
        name="", inline=False,
        value=""
    )

    embed.add_field(
        name=f"{weapon.effect_name}", inline=False,
        value=f"{weapon.true_description}"
    )

    if weapon.signature is not None:
        embed.add_field(
            name=f"", inline=False,
            value=f"** **\nThis is **"
                  f"{bot.valks[weapon.signature].icon.value} "
                  f"{bot.valks[weapon.signature].name}'s** signature W-Engine!"
        )

    embed.set_thumbnail(url=weapon.icon_image_url)
    embed.colour = int(weapon.embed_color, 16)

    return weapon, embed


def print_weapon(bot, weapon_id="13101"):
    weapon, embed = base_embed_and_load_weapon(weapon_id, bot)

    embed.set_field_at(
        name=f"Stats at Lv1 → Lv60", index=0,
        value=f"{weapon.print_mainstat()} {weapon.main_stat_base} → {weapon.get_mainstat_at_level(60)}\n"
              f"{weapon.print_substat()} {weapon.print_substat_at_level(0)} → {weapon.print_substat_at_level(60)}"
    )

    return embed


def print_weapon_at_level(bot, weapon_id="13101", level=60):
    weapon, embed = base_embed_and_load_weapon(weapon_id, bot)

    embed.set_field_at(
        name=f"Stats at Lv{level}", index=0,
        value=f"{weapon.print_mainstat()} {weapon.get_mainstat_at_level(level)}\n"
              f"{weapon.print_substat()} {weapon.print_substat_at_level(level)}"
    )

    return embed
