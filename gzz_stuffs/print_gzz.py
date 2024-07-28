from gzz_stuffs.print_valk import print_valk, print_valk_at_level
from gzz_stuffs.print_weapon import print_weapon, print_weapon_at_level


async def print_gzz(message):
    true_message = message.content[6:]

    if true_message.startswith("valk"):
        arguments = true_message.split()
        if len(arguments) == 1:
            await message.channel.send(embed=print_valk())
        elif len(arguments) == 2:
            await message.channel.send(embed=print_valk(arguments[1]))
        else:
            await message.channel.send(embed=print_valk_at_level(arguments[1], int(arguments[2])))

    elif true_message.startswith("weapon"):
        arguments = true_message.split()
        if len(arguments) == 1:
            await message.channel.send(embed=print_weapon())
        elif len(arguments) == 2:
            await message.channel.send(embed=print_weapon(arguments[1]))
        else:
            await message.channel.send(embed=print_weapon_at_level(arguments[1], int(arguments[2])))
