import discord

from gzz_stuffs.print_bangaloo import print_bangaloo, print_bangaloo_at_level
from gzz_stuffs.print_valk import print_valk, print_valk_at_level
from gzz_stuffs.print_weapon import print_weapon, print_weapon_at_level


signature_weapon = (
  " wep", "'s wep", "s wep",
  " weap", "'s weap", "s weap",
  " weapon", "'s weapon", "s weapon",
  " sig", "'s sig", "s sig",
  " sig wep", "'s sig wep", "sig wep",
  " sig weap", "'s sig weap", "sig weap",
  " sig weapon", "'s sig weapon", "s sig weapon",
  " signature", "'s signature", "s signature",
  " signature wep", "'s signature wep", "s signature wep",
  " signature weap", "'s signature weap", "s signature weap",
  " signature weapon", "'s signature weapon", "s signature weapon",
)


def print_ambiguous(bot, options):
    embed = discord.Embed(
        title=f"That search is ambiguous, possible options:"
    )

    embed_description = ""

    for item in options:
        item_type, item = figure_out_type(bot, item)
        if item_type == "Valk":
            embed_description = f"{embed_description}{bot.valks[item].icon.value} {bot.valks[item].full_name}\n"

        elif item_type == "Weapon":
            embed_description = f"{embed_description}{bot.weapons[item].icon.value} {bot.weapons[item].name}\n"

        elif item_type == "Bangaloo":
            embed_description = f"{embed_description}{bot.bangaloos[item].icon.value} {bot.bangaloos[item].name}\n"

    embed.description = embed_description[:-1]

    return embed


def figure_out_type(bot, id_to_look):
    if type(id_to_look) is list:
        return "Ambiguous", id_to_look

    if id_to_look in bot.valks:
        return "Valk", id_to_look

    if id_to_look in bot.weapons:
        return "Weapon", id_to_look

    if id_to_look in bot.bangaloos:
        return "Bangaloo", id_to_look

    return None, None


def get_weapon(bot, looking_for):
    true_looking_for = ""
    found_length = 0

    for item in signature_weapon:
        if looking_for.endswith(item) and len(item) > found_length:
            true_looking_for = looking_for[:-len(item)]
            found_length = len(item)

    if true_looking_for not in bot.translations or bot.translations[true_looking_for] not in bot.valks:
        return None, None

    valk_id = bot.translations[true_looking_for]
    valk = bot.valks[valk_id]
    return "Weapon", valk.signature_weapon


async def print_gzz(message, bot):
    true_message = message.content[6:]

    message_list = true_message.split()

    type_to_print = None
    what_to_print = None
    level_to_print = None

    if 0 < len(message_list) < 3 and message_list[0].isnumeric():
        type_to_print, what_to_print = figure_out_type(message_list[0], bot)

        if len(message_list) == 2 and message_list[-1].isnumeric():
            level_to_print = int(message_list[-1])

    else:
        looking_for = " ".join(message_list)

        if looking_for in bot.translations:
            type_to_print, what_to_print = figure_out_type(bot, bot.translations[looking_for])

        elif looking_for.endswith(signature_weapon):
            type_to_print, what_to_print = get_weapon(bot, looking_for)

        elif message_list[-1].isnumeric():
            level_to_print = int(message_list[-1])
            looking_for = " ".join(message_list[:-1])

        if looking_for in bot.translations:
            type_to_print, what_to_print = figure_out_type(bot, bot.translations[looking_for])

        elif looking_for.endswith(signature_weapon):
            type_to_print, what_to_print = get_weapon(bot, looking_for)

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
                await message.channel.send(embed=print_bangaloo(bot, what_to_print))
            else:
                await message.channel.send(embed=print_bangaloo_at_level(bot, what_to_print, level_to_print))

        elif type_to_print == "Ambiguous":
            await message.channel.send(embed=print_ambiguous(bot, what_to_print))

    else:
        await message.channel.send(f"Couldn't figure out what you wanted. Maybe ping mama keilo about it?")
        print(f"{message.author.name} tried this: {message.content}")
