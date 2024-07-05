import os
import requests
import math


HYPIXEL_API_KEY = os.environ.get("HYPIXEL_API_KEY")
PLAYER_API_LINK = f'https://api.hypixel.net/v2/player?key={HYPIXEL_API_KEY}&name='
GUILD_API_LINK = f'https://api.hypixel.net/v2/guild?key={HYPIXEL_API_KEY}&player='
STATUS_API_LINK = f'https://api.hypixel.net/v2/status?key={HYPIXEL_API_KEY}&uuid='

SKIN_LINK = "https://starlightskins.lunareclipse.studio/render/walking/" # Visit https://docs.lunareclipse.studio/ for documentation
ONLINE_LINK = "https://www.clker.com/cliparts/L/u/0/1/d/C/green-square-md.png"
OFFLINE_LINK = "https://www.clker.com/cliparts/h/8/f/t/N/a/deep-red-square-md.png"


def get_player_data(table, username: str) -> dict:
    id_user = username.lower()
    player_data: dict = (requests.get(f'{PLAYER_API_LINK}{username}')).json()
    if not player_data['success']:
        if player_data['cause'] == "You have already looked up this name recently":
            response = table.get_item(Key={"player_name": id_user})
            if "Item" not in response: return [False, make_error_embed(501, f"**{reformat_username(username)}**'s dataset was found but unable to retrieve it. Try again in 1 minute!")]
            player_data = response["Item"]["cache_data"]
            return [True, player_data["General"]]
        elif player_data['cause'] == "Invalid API key": return [False, make_error_embed(403, "The current API Key is invalid. A new API Key is required!")]
        elif player_data['cause'] == "Key throttle": return [False, make_error_embed(429, "The number of API requests exceeded the threshold! Try again in 5 mins!")]
        else: return [False, make_error_embed(900, "Unknown Error")]
    if player_data['player'] is None: return [False, make_error_embed(201, f"**{reformat_username(username)}** does not exist in Hypixel's Databases!")]
    
    if table.item_count >= 64:
        scan = table.scan()
        with table.batch_writer() as batch:
            for each in scan['Items']:
                batch.delete_item(Key={'player_name': each['player_name']})
        
    if "stats" not in player_data['player'] or "Arcade" not in player_data['player']['stats']: 
        player_data['player']['stats'] = { "Arcade": {} }
    arcade_data = player_data['player']['stats']['Arcade']
    
    guild_data: dict = (requests.get(f'{GUILD_API_LINK}{player_data["player"]["uuid"]}')).json()
    
    session = "in Invisible Mode"
    if "lastLogin" in player_data['player']:
        status_data = requests.get(f'{STATUS_API_LINK}{player_data["player"]["uuid"]}').json()
        if status_data['success'] and status_data['session']['online']:
            session = f"in {format_word(status_data['session']['gameType'])}: {format_word(status_data['session']['mode'])}"
        else: session = "Offline"
    
    header = f"{check_rank(player_data['player'], 'newPackageRank')}{reformat_username(player_data['player']['displayname'])}"
    skin_link = f"{SKIN_LINK}{player_data['player']['uuid']}/full"
    session_img_link = OFFLINE_LINK if session == "Offline" or session == "in Invisible Mode" else ONLINE_LINK
    session_text = f"Currently {session}\nBot is NOT affiliated or endorsed by Hypixel"
    
    zombies_data = {
        "General": {
            "title": header,
            "description": "General Statistics",
            "color": 0x9C9C9C,  # Lighter Gray
            "thumbnail": { "url": skin_link },
            "fields": [
                {"name": "\nNetwork Statistics", "value": ""},
                {"name": "Level\t\t\t\t\t\t\t\t‎",  "value": f"```{network_exp_level(player_data['player']['networkExp'])}```",         "inline": True},
                {"name": "Achievement Points‎",     "value": f"```{check_num(player_data['player'],'achievementPoints')}```",           "inline": True},
                {"name": "Language\t\t\t\t\t‎",     "value": f"```{check_language(player_data['player'], 'userLanguage')}```",          "inline": True},    
                
                {"name": "", "value": ""},
                {"name": f"Guild Name {'- ' + format(len(guild_data['guild']['members']), ',') + ' Mbrs.' if guild_data['success'] and guild_data['guild'] else ''}\t\t‎", "value": f"```{guild_data['guild']['name'] if guild_data['success'] and guild_data['guild'] else 'N/A'}```", "inline": True},
                {"name": "Levels\t‎",              "value": f"```{guild_exp_to_level(guild_data['guild']['exp']) if guild_data['success'] and guild_data['guild'] else 'N/A'}```", "inline": True},
                {"name": "‎", "value": ""},
                
                {"name": "Zombies Statistics",      "value": f""},
                {"name": "Grade Score",             "value": "```WIP```", "inline": True},
                {"name": "Wins",                    "value": f"```{check_num(arcade_data, 'wins_zombies')}```",                                             "inline": True},
                {"name": "Total Rounds Surv.",      "value": f"```{check_num(arcade_data, 'total_rounds_survived_zombies')}```",                            "inline": True},
                {"name": "Hit Accuracy",            "value": f"```{check_ratio(arcade_data, 'bullets_hit_zombies', 'bullets_shot_zombies', True)}%```",     "inline": True},
                {"name": "Headshots Accuracy",      "value": f"```{check_ratio(arcade_data, 'headshots_zombies', 'bullets_hit_zombies', True)}%```",        "inline": True},
                {"name": "Kill/Death Ratio",        "value": f"```{check_ratio(arcade_data, 'zombie_kills_zombies', 'deaths_zombies', False)}```",          "inline": True},
                {"name": "Kills",                   "value": f"```{check_num(arcade_data, 'zombie_kills_zombies')}```",                                     "inline": True},
                {"name": "Downs",                   "value": f"```{check_num(arcade_data, 'times_knocked_down_zombies')}```",                               "inline": True},
                {"name": "Deaths",                  "value": f"```{check_num(arcade_data, 'deaths_zombies')}```",                                           "inline": True},
                {"name": "Revives",                 "value": f"```{check_num(arcade_data, 'players_revived_zombies')}```",                                  "inline": True},
                {"name": "Doors Opened",            "value": f"```{check_num(arcade_data, 'doors_opened_zombies')}```",                                     "inline": True},
                {"name": "Windows Repaired",        "value": f"```{check_num(arcade_data, 'windows_repaired_zombies')}```",                                 "inline": True},
            ],
            "footer": { "text": session_text, "icon_url": session_img_link }
        }, 
        "Dead End": {
            "General": generate_embed(arcade_data, "deadend", "g", header, skin_link, session_img_link, session_text),
            "Normal": generate_embed(arcade_data, "deadend", "normal", header, skin_link, session_img_link, session_text),
            "Hard": generate_embed(arcade_data, "deadend", "hard", header, skin_link, session_img_link, session_text),
            "RIP": generate_embed(arcade_data, "deadend", "rip", header, skin_link, session_img_link, session_text)
        },
        "Bad Blood": {
            "General": generate_embed(arcade_data, "badblood", "g", header, skin_link, session_img_link, session_text),
            "Normal": generate_embed(arcade_data, "badblood", "normal", header, skin_link, session_img_link, session_text),
            "Hard": generate_embed(arcade_data, "badblood", "hard", header, skin_link, session_img_link, session_text),
            "RIP": generate_embed(arcade_data, "badblood", "rip", header, skin_link, session_img_link, session_text)
        },
        "Alien Arcadium": {
            "title": header,
            "description": "Alien Arcadium Zombies Statistics",
            "color": 0x5865F2,  # Blurple
            "thumbnail": { "url": skin_link },
            "fields": [
                {"name": "Grade Score\t\t\t\t\t ‎",      "value": "```WIP```",                                                                           "inline": True},
                {"name": "Wins\t\t\t\t\t\t\t\t   ‎",     "value": f"```{check_num(arcade_data, 'wins_zombies_alienarcadium_normal')}```",                "inline": True},
                {"name": "Best Rounds\t\t\t\t\t ‎",      "value": f"```{check_num(arcade_data, 'best_round_zombies_alienarcadium')}```",                 "inline": True},
                {"name": "Total Rounds Surv.",                  "value": f"```{check_num(arcade_data, 'total_rounds_survived_zombies_alienarcadium')}```",      "inline": True},
                {"name": "Fastest Time by R10",                 "value": f"```{check_time(arcade_data, 'fastest_time_10_zombies_alienarcadium_normal')}```",    "inline": True},
                {"name": "Fastest Time by R20",                 "value": f"```{check_time(arcade_data, 'fastest_time_20_zombies_alienarcadium_normal')}```",    "inline": True},
                {"name": "Kills",                               "value": f"```{check_num(arcade_data, 'zombie_kills_zombies_alienarcadium')}```",               "inline": True},
                {"name": "Downs",                               "value": f"```{check_num(arcade_data, 'times_knocked_down_zombies_alienarcadium')}```",         "inline": True},
                {"name": "Deaths",                              "value": f"```{check_num(arcade_data, 'deaths_zombies_alienarcadium')}```",                     "inline": True},
                {"name": "Revives",                             "value": f"```{check_num(arcade_data, 'players_revived_zombies_alienarcadium')}```",            "inline": True},
                {"name": "Doors Opened",                        "value": f"```{check_num(arcade_data, 'doors_opened_zombies_alienarcadium')}```",               "inline": True},
                {"name": "Windows Repaired",                    "value": f"```{check_num(arcade_data, 'windows_repaired_zombies_alienarcadium')}```",           "inline": True},
            ],
            "footer": { "text": session_text, "icon_url": session_img_link }
        },
        "Prison": {
            "General": generate_embed(arcade_data, "prison", "g", header, skin_link, session_img_link, session_text),
            "Normal": generate_embed(arcade_data, "prison", "normal", header, skin_link, session_img_link, session_text),
            "Hard": generate_embed(arcade_data, "prison", "hard", header, skin_link, session_img_link, session_text),
            "RIP": generate_embed(arcade_data, "prison", "rip", header, skin_link, session_img_link, session_text)
        }
    }
    
    table.put_item(Item={"player_name": id_user, "cache_data": zombies_data})
    return [True, zombies_data["General"]]


def get_player_data_from_aws_db(table, username: str, args: list[str]):
    id_user = username.lower()
    response = table.get_item(Key={"player_name": id_user})
    if "Item" not in response: return [False, make_error_embed(502, f"Uable to retrieve **{reformat_username(username)}**'s dataset from DynamoDB")]
    player_data = response["Item"]["cache_data"]
    
    map_name, mode_type = "", ""
    if args[0] == "g": return [True, player_data["General"]]
    if args[0] == "aa": return [True, player_data["Alien Arcadium"]]
    
    if args[0] == "de": map_name = "Dead End"
    elif args[0] == "bb": map_name = "Bad Blood"
    elif args[0] == "p": map_name = "Prison"
    if args[1] == "g": mode_type = "General"
    elif args[1] == "n": mode_type = "Normal"
    elif args[1] == "h": mode_type = "Hard"
    elif args[1] == "r": mode_type = "RIP"
    
    return [True, player_data[map_name][mode_type]]
   

def generate_embed(arcade_data: dict, map: str, mode: str, header: str, skin_link: str, session_img_link: str, session_text: str):
    map_colors = { "deadend": 0x008080, "badblood": 0x8B0000, "prison": 0x8B7000 }
    mode_colors = { "normal": 0x1DB954, "hard": 0xAEC202, "rip": 0xC20202 }
    map_title = { "deadend": "Dead End", "badblood": "Bad Blood", "prison": "Prison" }
    mode_title = {"normal": "Normal", "hard": "Hard", "rip": "RIP"}
    
    if mode == "g":
        embed = {
            "title": header,
            "description": f"General {map_title[map]} Zombies Statistics",
            "color": map_colors[map], 
            "thumbnail": { "url": skin_link },
            "fields": [
                {"name": "Grade Score\t\t\t‎",       "value": "```WIP```",                                                                       "inline": True},
                {"name": "Wins\t\t\t\t\t\t\t\t‎",    "value": f"```{check_num(arcade_data, f'wins_zombies_{map}')}```",                          "inline": True},
                {"name": "Total Rounds Surv.\t‎",    "value": f"```{check_num(arcade_data, f'total_rounds_survived_zombies_{map}')}```",         "inline": True},
                {"name": "Normal Best Rounds",              "value": f"```{check_num(arcade_data, f'best_round_zombies_{map}_normal')}```",             "inline": True},
                {"name": "Hard Best Rounds",                "value": f"```{check_num(arcade_data, f'best_round_zombies_{map}_hard')}```",               "inline": True},
                {"name": "RIP Best Rounds",                 "value": f"```{check_num(arcade_data, f'best_round_zombies_{map}_rip')}```",                "inline": True},
                {"name": "Normal FTB R30",                  "value": f"```{check_time(arcade_data, f'fastest_time_30_zombies_{map}_normal')}```",       "inline": True},
                {"name": "Hard FTB R30",                    "value": f"```{check_time(arcade_data, f'fastest_time_30_zombies_{map}_hard')}```",         "inline": True},
                {"name": "RIP FTB R30",                     "value": f"```{check_time(arcade_data, f'fastest_time_30_zombies_{map}_rip')}```",          "inline": True},
                {"name": "Kills",                           "value": f"```{check_num(arcade_data, f'zombie_kills_zombies_{map}')}```",                  "inline": True},
                {"name": "Deaths",                          "value": f"```{check_num(arcade_data, f'deaths_zombies_{map}')}```",                        "inline": True},
                {"name": "Revives",                         "value": f"```{check_num(arcade_data, f'players_revived_zombies_{map}')}```",               "inline": True},
            ],
            "footer": { "text": session_text, "icon_url": session_img_link }
        }
    else:
        embed = {
            "title": header,
            "description": f"[{mode_title[mode]}] {map_title[map]} Zombies Statistics",
            "color": mode_colors[mode],
            "thumbnail": { "url": skin_link },
            "fields": [
                {"name": "Wins\t\t\t\t\t\t\t\t‎",    "value": f"```{check_num(arcade_data, f'wins_zombies_{map}_{mode}')}```",                   "inline": True},
                {"name": "Best Rounds\t\t\t\t‎",     "value": f"```{check_num(arcade_data, f'best_round_zombies_{map}_{mode}')}```",             "inline": True},
                {"name": "Total Rounds Surv.\t‎",    "value": f"```{check_num(arcade_data, f'total_rounds_survived_zombies_{map}_{mode}')}```",  "inline": True},
                {"name": "Fastest Time by R10",             "value": f"```{check_time(arcade_data, f'fastest_time_10_zombies_{map}_{mode}')}```",       "inline": True},
                {"name": "Fastest Time by R20",             "value": f"```{check_time(arcade_data, f'fastest_time_20_zombies_{map}_{mode}')}```",       "inline": True},
                {"name": "Fastest Time by R30",             "value": f"```{check_time(arcade_data, f'fastest_time_30_zombies_{map}_{mode}')}```",       "inline": True},
                {"name": "Kills",                           "value": f"```{check_num(arcade_data, f'zombie_kills_zombies_{map}_{mode}')}```",           "inline": True},
                {"name": "Downs",                           "value": f"```{check_num(arcade_data, f'times_knocked_down_zombies_{map}_{mode}')}```",     "inline": True},
                {"name": "Deaths",                          "value": f"```{check_num(arcade_data, f'deaths_zombies_{map}_{mode}')}```",                 "inline": True},
                {"name": "Revives",                         "value": f"```{check_num(arcade_data, f'players_revived_zombies_{map}_{mode}')}```",        "inline": True},
                {"name": "Doors Opened",                    "value": f"```{check_num(arcade_data, f'doors_opened_zombies_{map}_{mode}')}```",           "inline": True},
                {"name": "Windows Repaired",                "value": f"```{check_num(arcade_data, f'windows_repaired_zombies_{map}_{mode}')}```",       "inline": True}
            ],
            "footer": { "text": session_text, "icon_url": session_img_link }
        }
    return embed


def check_num(stats: dict, key: str):
    if key in stats: return format(stats[key], ",")
    else: return "0"   


def check_rank(stats: dict, key: str) -> str:
    if key in stats:
        rank = stats[key].replace("_PLUS", "+")
        if "monthlyPackageRank" in stats and stats['monthlyPackageRank'] != "NONE": rank = "MVP++"
        return f"[{rank}] "
    return ""


def check_language(stats: dict, key: str):
    if key in stats: return format_word(stats[key])
    return "English"


def check_ratio(stats: dict, upper_key: str, lower_key: str, percent: bool):
    numerator, denominator = 0, 1
    if upper_key in stats: numerator = stats[upper_key]
    if lower_key in stats: denominator = stats[lower_key]
    return round(numerator/denominator * (100 if percent else 1))


def check_time(stats: dict, key: str):
    if key not in stats: return "00:00"
    timer = stats[key]
    if timer < 3600: return f"{str(math.floor(timer / 60)).zfill(2)}:{str(math.floor((timer % 60))).zfill(2)}"
    else: return f"{math.floor(timer / 3600)}:{str(math.floor((timer % 3600) / 60)).zfill(2)}:{str(math.floor((timer % 60))).zfill(2)}"


def format_word(word: str):
    words = word.split('_')
    formatted_words = [word.capitalize() for word in words] # Capitalize the first character of each word and lowercase the rest
    formatted_game_type = ' '.join(formatted_words)
    return formatted_game_type


def reformat_username(name: str):
    reformatted_name = ""
    for i in range(len(name)):
        if name[i] == "_": reformatted_name += "\_"
        else: reformatted_name += name[i]
    return reformatted_name


def network_exp_level(exp: int):
    return format(math.floor((math.sqrt(2*exp+30625)/50)-2.5), ",")
  
   
def guild_exp_to_level(exp: int):
    if exp < 100000: return 0
    elif exp < 250000: return 1
    elif exp < 500000: return 2
    elif exp < 1000000: return 3
    elif exp < 1750000: return 4
    elif exp < 2750000: return 5
    elif exp < 4000000: return 6
    elif exp < 5500000: return 7
    elif exp < 7500000: return 8
    elif exp < 15000000: return (exp - 7500000) // 2500000 + 9
    else: return format(((exp - 15000000) // 3000000 + 12), ",")
    
def make_error_embed(num: int = 0, error_msg: str = "") -> dict:
    embed = {
        "title": f"❌ ERROR {num}",
        "description": error_msg,
        "color": 0xFF0000  # Red color
    }
    return embed







