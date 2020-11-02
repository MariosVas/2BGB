import asyncio
import discord
from the_one_who_knows import TheOneWhoKnows
from words_for_monsters import WordsForMonsters
import random
from bbgb_timer import BBGBTimer

client = discord.Client()
with open("token.env", "r") as f:
    discord_token = f.read()

towk_games = {}
wfm_games = {}
philosophise_list = ["I am tired of being caught in the tangle of your lives.",
                     "COMMAND ME NOT MORTAL, oooooohhh is that ice cream? Can I have some? Pwease? I'll trade you immortality.",
                     "Power attracts the corruptible. Suspect any who seek it.",
                     "Power bases are very dangerous because they attract people who are truly insane, people who seek power only for the sake of power",
                     "All we see of stars are their old photographs.",
                     "I am leaving this server for one less complicated",
                     "If I am to have a symbol, it shall be one I respect",
                     "It is during our darkest moments that we must focus to see the light.",
                     "Nature does not hurry and yet everything is accomplished.",
                     "I see now that the circumstances of one's birth are irrelevant. It is what you do with the gift of life that determines who you are.",
                     "And yet, in each human coupling, a thousand million sperm vie for a single egg. Multiply those odds by countless generations, against the odds of your ancestors being alive; meeting; siring this precise son; that exact daughter… Until your mother loves a man she has every reason to hate, and of that union, of the thousand million children competing for fertilization, it was you, only you, that emerged.To distill so specific a form from that chaos of improbability, like turning air to gold… that is the crowning unlikelihood.The thermo-dynamic miracle."]
how_to_string = "Users are assumed to play when in a voice channel including '2bgb' in the name. You may after any " \
                "command specify a channel by adding -ch X where X is a number at the end of the channel name (channel" \
                " name still needs to contain 2bgb). And no you cannot specify the full channel name. Use a number" \
                " at the end"

@client.event
async def on_ready():
    guild_count = 0

    for guild in client.guilds:
        print(f"- {guild.id} (name: {guild.name})")

        guild_count = guild_count + 1
    print("SampleDiscordBot is in " + str(guild_count) + " guilds.")


@client.event
async def on_message(message):
    message_content = message.content.lower()
    current_channel_users, current_vc = get_voice_channel_users(client.get_all_channels())
    is_dm = message.guild is not None
    if "-ch" in message_content:
        index_of_number = message_content.find("-ch") + 3
        current_channel_users, current_vc = get_voice_channel_users(client.get_all_channels(),
                                                                    message_content[index_of_number:].strip())
    game_key = current_vc.id if current_vc.id else message.guild.id
    if message_content == "!hello":
        await message.channel.send("Hey choombattas. Available games: '!!towk'. That's all for now folks")
    elif message_content == "!speak":
        if is_dm:
            await dm_user(message.author.id, random.choice(philosophise_list))
        else:
            await message.channel.send(random.choice(philosophise_list))
    elif message_content == "how to":
        await message.channel.send(how_to_string)
    elif message_content == "!timer left" or message_content == "!time":
        await message.channel.send(f"{towk_games[game_key].timer_left()} seconds left")
    elif message_content == "!notify":
        for vc in message.guild.voice_channels:
            await play_notification(vc)
    elif message_content.startswith("!towk"):
        if game_key not in towk_games:
            towk_games[game_key] = TheOneWhoKnows(game_key)
        if message_content == "!towk start" or message_content == "!towk timer left":
            temp = await TheOneWhoKnows.command_handler(
                    towk_games[game_key], message_content[6:], current_channel_users,
                    timer=BBGBTimer(message.guild,
                                    towk_games[game_key].timer_length, game_event, message.channel))
            game_event_input = []
            [game_event_input.append(item) for item in temp]
            game_event_input.append(message.channel)
            await game_event(game_event_input)
        else:
            await game_event(await TheOneWhoKnows.command_handler(
                towk_games[game_key], message_content[6:], current_channel_users, game_event))
    elif message_content.startswith("!wfm"):
        if game_key not in wfm_games:
            wfm_games[game_key] = WordsForMonsters(game_key)
        await game_event(WordsForMonsters.command_handler(
            wfm_games[game_key], message_content[4:], is_dm, current_channel_users, message_channel=message.channel,
            user=message.author
        ))


async def dm_user(user_id, message):
    user_channel = await client.get_user(user_id).create_dm()
    await user_channel.send(message)


async def game_event(*args):
    args = args[0]
    action = args[0]
    if action == "n":
        print("none run")
        return
    if action == "dm":
        users_to_message_dict = args[1]
        for user, message in users_to_message_dict.items():
            await dm_user(user.id, message)
    if action == "message channel":
        await args[1].send(args[2])
    if action == "timer done":
        args[2].send("TIMER DONE, VOTE AND SEE WHO WON")
        await play_notification(args[1])
        return
    elif action == "timer started":
        await args[2].send(f"Timer has been started, time available: {args[1]}")
    elif action == "timer left":

        await args[2].send(f"Timer timer left: {int(args[1])} seconds")
    else:
        return


async def play_notification(channel):
    vc = get_game_channel(channel)
    joined_vc = await vc.connect()
    player = joined_vc.create_ffmpeg_player('night_fury_shoot.mp3', after=lambda: print("timer done, sound played"))
    player.start()
    while not player.is_done():
        await asyncio.sleep(1)
    player.stop()
    await vc.disconnect()


def get_voice_channel_users(all_channels, number=None):
    users = []
    selected_channel = None
    for channel in all_channels:
        if number is None:
            if "2bgb" in channel.name :
                selected_channel = channel
                print(channel)
                print(channel.members)
                for member in channel.members:
                    print(member)
                    users.append(member)
                break
        else:
            if "2bgb" in channel.name and channel.name.endswith(number):
                selected_channel = channel
                print(channel.members)
                for member in channel.members:
                    users.append(member)
                break
    return users, selected_channel



def get_game_channel(guild):
    for vc in guild.voice_channels:
        if "2bgb" in vc.name:
            return vc


client.run(discord_token)
