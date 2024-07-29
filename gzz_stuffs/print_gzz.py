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


def figure_out_type(id, json):
    if id in json["valks"]:
        return "Valk", id

    elif id in json["weapons"]:
        return "Weapon", id

    elif id in json["bangaloos"]:
        return "Bangaloo", id

    return None, None


def get_weapon(looking_for, translations_json):
    true_looking_for = ""

    for item in signature_weapon:
        if looking_for.endswith(item):
            true_looking_for = looking_for[:-len(item)]

    if true_looking_for not in translations_json:
        return None, None

    valk = translations_json["true_looking_for"]


async def print_gzz(message):
    true_message = message.content[6:]

    with open("gzz_stuffs/util/ids.json", "r", encoding="utf-8") as ids_json_file:
        ids_json = json.load(ids_json_file)

    with open("gzz_stuffs/util/translations.json", "r", encoding="utf-8") as translations_json_file:
        translations_json = json.load(translations_json_file)

    message_list = re.split("\s", true_message)

    type_to_print = None
    what_to_print = None
    level_to_print = None

    if 0 < len(message_list) < 3 and message_list[0].isnumeric():
        type_to_print, what_to_print = figure_out_type(message_list[0], ids_json)

        if len(message_list) == 2 and message_list[-1].isnumeric():
            level_to_print = int(message_list[-1])

    else:
        looking_for = " ".join(message_list)

        if message_list[-1].isnumeric():
            level_to_print = int(message_list[-1])
            looking_for = " ".join(message_list[:-1])

        if looking_for in translations_json:
            type_to_print, what_to_print = figure_out_type(translations_json[looking_for], ids_json)

        if looking_for.endswith(signature_weapon):
            type_to_print, what_to_print = get_weapon(looking_for, translations_json)

    if type_to_print is not None:
        if type_to_print == "Valk":
            if level_to_print is None:
                await message.channel.send(embed=print_valk(what_to_print))
            else:
                await message.channel.send(embed=print_valk_at_level(what_to_print, level_to_print))

        elif type_to_print == "Weapon":
            if level_to_print is None:
                await message.channel.send(embed=print_weapon(what_to_print))
            else:
                await message.channel.send(embed=print_weapon_at_level(what_to_print, level_to_print))

        elif type_to_print == "Bangaloo":
            if level_to_print is None:
                await message.channel.send(f"Tried to print {what_to_print}, but bangboos are not implemented yet")
            else:
                await message.channel.send(f"Tried to print {what_to_print} at lv{level_to_print}, "
                                           f"but bangboos are not implemented yet")

    else:
        await message.channel.send(f"Couldn't figure out what you wanted. Maybe ping mama keilo about it?")
        print(message.content)
