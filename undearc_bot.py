import random
import re
import discord
import json
import os
import markovify

from gzz_stuffs.print_gzz import print_gzz
from gzz_stuffs.util.Valk import Valk
from gzz_stuffs.util.Weapon import Weapon


class Underarc:
    id = 963273616353550367
    guild = None

    people_identities = {}
    extraction_channels = []
    signed_up = []
    answers_8ball = []
    admins = []

    valks = {}
    weapons = {}
    bangaloos = {}
    translations = {}

    def load_gzz_stuffs(self):
        with open("gzz_stuffs/util/translations.json", "r", encoding="utf-8") as translations_json_file:
            self.translations = json.load(translations_json_file)

        with open("gzz_stuffs/util/ids.json", "r", encoding="utf-8") as ids_json_file:
            all_ids = json.load(ids_json_file)

        with open(f"gzz_stuffs/util/valk_extra_infos.json", "r", encoding="utf-8") as valk_extra_stuffs_json_file:
            valk_extra_stuffs_json = json.load(valk_extra_stuffs_json_file)

        for valk in all_ids["valks"]:
            with open(f"gzz_stuffs/valks/{valk}.json", "r", encoding="utf-8") as valk_json_file:
                self.valks[valk] = Valk(json.load(valk_json_file), valk_extra_stuffs_json)

        with open(f"gzz_stuffs/util/weapon_extra_infos.json", "r", encoding="utf-8") as weapon_extra_stuffs_json_file:
            weapon_extra_stuffs_json = json.load(weapon_extra_stuffs_json_file)

        for weapon in all_ids["weapons"]:
            with open(f"gzz_stuffs/weapons/{weapon}.json", "r", encoding="utf-8") as weapon_json_file:
                self.weapons[weapon] = Weapon(json.load(weapon_json_file), weapon_extra_stuffs_json)

        with open(f"gzz_stuffs/util/bangaloo_extra_infos.json", "r", encoding="utf-8") as bangaloo_extra_stuffs_json_file:
            bangaloo_extra_stuffs_json = json.load(bangaloo_extra_stuffs_json_file)

        for bangaloo in all_ids["bangaloos"]:
            with open(f"gzz_stuffs/bangaloos/{bangaloo}.json", "r", encoding="utf-8") as bangaloo_json_file:
                self.bangaloos[bangaloo] = {
                    "datamined_json": json.load(bangaloo_json_file),
                    "extra_stuffs": None
                }

    def load_extraction_channels(self):
        with open("markov_chain_stuffs/extraction_channels.json", "r", encoding="utf-8") as extraction_channels_json_file:
            self.extraction_channels = json.load(extraction_channels_json_file)["channels"]

    def load_signed_up(self):
        with open("markov_chain_stuffs/peep_list.json", "r", encoding="utf-8") as signed_up_json_file:
            self.signed_up = json.load(signed_up_json_file)["peeps"]

    def load_8ball_answers(self):
        with open("8ball_stuffs/8ball_answers.json", "r", encoding="utf-8") as answers_8ball_json_file:
            self.answers_8ball = json.load(answers_8ball_json_file)["answers"]

    def load_peoples_identities(self):
        for person in os.listdir("markov_chain_stuffs/people_identities"):
            with open(f"markov_chain_stuffs/people_identities/{person}", "r", encoding="utf-8") as person_file:
                self.people_identities[f"{person.split('.')[0]}"] = person_file.read()

    def load_admins(self):
        with open("admins.json", "r", encoding="utf-8") as admins_json_file:
            self.admins = json.load(admins_json_file)["admins"]


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

underarc = Underarc()

approved_command_channels = [1183484161063927881, 1169933053376864287, 966951945103347794, 1265927569627414620]


async def extract_messages(limit=None):
    for user in underarc.signed_up:
        underarc.people_identities[f"{user}"] = ""

    for channel_id in underarc.extraction_channels:
        channel = discord.utils.get(underarc.guild.channels, id=channel_id)
        print(f"doing {channel}")

        async for message in channel.history(limit=limit):
            if f"{message.author.id}" in underarc.signed_up:
                filtered_message = filter_message(message.content)

                if filtered_message != "":
                    underarc.people_identities[f"{message.author.id}"] += f"{filtered_message}\n"

    print(underarc.people_identities)


def filter_message(message):
    cleaned_up_string = message.replace("|", "").replace("\"", "")
    cleaned_up_string = re.sub(
        r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+''' +
        r'''|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+''' +
        r'''|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''',
        "",
        cleaned_up_string
    )

    if cleaned_up_string.startswith("!alias"):
        return ""

    if cleaned_up_string.startswith("?warn"):
        return ""

    if cleaned_up_string.startswith("?mute"):
        return ""

    if cleaned_up_string.startswith(",. "):
        return ""

    if cleaned_up_string.startswith(",.. "):
        return ""

    return cleaned_up_string


def save_people_identities():
    for person, messages in underarc.people_identities.items():
        person_file = open(f"markov_chain_stuffs/people_identities/{person}.txt", "w", encoding="utf-8")
        person_file.write(messages)
        person_file.close()


@client.event
async def on_ready():
    underarc.guild = discord.utils.get(client.guilds, id=underarc.id)
    underarc.load_8ball_answers()
    underarc.load_extraction_channels()
    underarc.load_signed_up()
    underarc.load_admins()
    underarc.load_gzz_stuffs()

    underarc.load_peoples_identities()

    print(f"logged in {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.id in approved_command_channels and message.content.startswith(".arcy"):
        await print_gzz(message, underarc)

    elif message.channel.id in approved_command_channels and message.content.startswith("arcy"):
        true_message = message.content[5:]

        if true_message.startswith("8ball"):
            await message.channel.send(random.choice(underarc.answers_8ball))

        elif true_message.startswith("kys") and message.author.id in underarc.admins:
            await message.channel.send("o-okay ;_;")
            await client.close()

        elif true_message.startswith("math "):
            await message.channel.send(f"**I GOT THE TECH:** {eval(message.content[10:]):.2f}")

        elif true_message.startswith("update 8ball"):
            underarc.load_8ball_answers()

        elif true_message.startswith("update gzz"):
            underarc.load_gzz_stuffs()

        elif true_message.startswith("save identities"):
            save_people_identities()
            await message.channel.send("Saved everyone's identities!")

        elif true_message.startswith("load identities"):
            underarc.load_peoples_identities()

        elif true_message.startswith("generate"):
            # text_model = markovify.Text(underarc.people_identities[f"{message.author.id}"])
            # text_model.make_short_sentence(200, state_size=5)
            await message.channel.send("mama keilo prohibits me from doing this")

        elif true_message.startswith("extract"):
            limit = None
            if len(message.content.split()) == 2:
                limit = int(message.content.split()[1])

            await extract_messages(limit)

            await message.channel.send(f"Finished extracting messages!")

    if message.channel.id in underarc.extraction_channels and f"{message.author.id}" in underarc.signed_up:
        if f"{message.author.id}" in underarc.people_identities:
            underarc.people_identities[f"{message.author.id}"] += f"{message.content}\n"
        else:
            underarc.people_identities[f"{message.author.id}"] = f"{message.content}\n"

client.run("MTE4MzQ4MDY3MDgwMzIxMDI4Mg.GeWtwA.cQLIC_DUAhwGBExhs5p6tINRbvT4jZwsihd4ic")
