import json

from gzz_stuffs.print_valk import print_valk, print_valk_at_level
from gzz_stuffs.print_weapon import print_weapon, print_weapon_at_level
import re


signature_weapon = (
  " weap", "'s weap", "s weap",
  " weapon", "'s weapon", "s weapon",
  " sig", "'s sig", "s sig",
  " sig weap", "'s sig weap", "sig weap",
  " sig weapon", "'s sig weapon", "s sig weapon",
  " signature", "'s signature", "s signature",
  " signature weap", "'s signature weap", "s signature weap",
  " signature weapon", "'s signature weapon", "s signature weapon",
)


def figure_out_type(id, bot):
    if id in bot.valks:
        return "Valk", id

    elif id in bot.weapons:
        return "Weapon", id

    elif id in bot.bangaloos:
        return "Bangaloo", id

    return None, None


def get_weapon(looking_for, bot):
    true_looking_for = ""
    found_length = 0

    for item in signature_weapon:
        if looking_for.endswith(item) and len(item) > found_length:
            true_looking_for = looking_for[:-len(item)]
            found_length = len(item)

    if true_looking_for not in bot.translations:
        return None, None

    valk_id = bot.translations[true_looking_for]
    valk = bot.valks[valk_id]
    return "Weapon", valk.signature_weapon


async def print_gzz(message, bot):
    true_message = message.content[6:]

    message_list = re.split("\s", true_message)

    type_to_print = None
    what_to_print = None
    level_to_print = None

    if 0 < len(message_list) < 3 and message_list[0].isnumeric():
        type_to_print, what_to_print = figure_out_type(message_list[0], bot)

        if len(message_list) == 2 and message_list[-1].isnumeric():
            level_to_print = int(message_list[-1])

    else:
        looking_for = " ".join(message_list)

        if message_list[-1].isnumeric():
            level_to_print = int(message_list[-1])
            looking_for = " ".join(message_list[:-1])

        if looking_for in bot.translations:
            type_to_print, what_to_print = figure_out_type(bot.translations[looking_for], bot)

        if looking_for.endswith(signature_weapon):
            type_to_print, what_to_print = get_weapon(looking_for, bot)

    if type_to_print is not None:
        if type_to_print == "Valk":
            if level_to_print is None:
                await message.channel.send(embed=print_valk(bot, what_to_print))
            else:
                await message.channel.send(embed=print_valk_at_level(bot, what_to_print, level_to_print))

        elif type_to_print == "Weapon":
            if level_to_print is None:
                await message.channel.send(embed=print_weapon(bot, what_to_print))
            else:
                await message.channel.send(embed=print_weapon_at_level(bot, what_to_print, level_to_print))

        elif type_to_print == "Bangaloo":
            if level_to_print is None:
                await message.channel.send(f"Tried to print {what_to_print}, but bangboos are not implemented yet")
            else:
                await message.channel.send(f"Tried to print {what_to_print} at lv{level_to_print}, "
                                           f"but bangboos are not implemented yet")

    else:
        await message.channel.send(f"Couldn't figure out what you wanted. Maybe ping mama keilo about it?")
        print(message.content)
