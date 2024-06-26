import os
import requests
import math


HYPIXEL_API_KEY = os.environ.get("HYPIXEL_API_KEY")
PLAYER_API_LINK = f'https://api.hypixel.net/v2/player?key={HYPIXEL_API_KEY}&name='
GUILD_API_LINK = f'https://api.hypixel.net/v2/guild?key={HYPIXEL_API_KEY}&player='
STATUS_API_LINK = f'https://api.hypixel.net/v2/status?key={HYPIXEL_API_KEY}&uuid='

def get_player_data(username: str):
      player_data: dict = (requests.get(f'{PLAYER_API_LINK}{username}')).json()
      
      if not player_data['success']:
            return player_data
      if player_data['player'] is None:
            player_data = { "success": False, "cause": "Player data does not exist" }
            return player_data
      
      formatted_player_data = {
            "success": True,
            "Data": {
                  "Name": player_data['player']['displayname'], 
                  "UUID": player_data['player']['uuid'], 
                  "Rank": fix_rank_title(player_data['player'], 'newPackageRank'),
                  "Network Level": math.floor((math.sqrt(2*player_data['player']['networkExp']+30625)/50)-2.5),
                  "Achievement Points": fix_key_error(player_data['player'],'achievementPoints'),
                  "Language":  format_lanauge(player_data['player'], 'userLanguage'),
            }
      }
      
      guild_data: dict = (requests.get(f'{GUILD_API_LINK}{player_data["player"]["uuid"]}')).json()
      if guild_data['success'] and guild_data['guild']:
            formatted_guild_data = {
                  "Name": guild_data['guild']['name'],
                  "Level": guild_level(guild_data['guild']['exp']),
                  "Members": len(guild_data['guild']['members']),
            }
            formatted_player_data['Data']['Guild'] = formatted_guild_data
      else: formatted_player_data['Data']['Guild'] = None
      
      if "lastLogin" in player_data['player']:
            status_data = requests.get(f'{STATUS_API_LINK}{player_data["player"]["uuid"]}').json()
            if status_data['success'] and status_data['session']['online']:
                  game_type = format_name(status_data['session']['gameType'])
                  formatted_player_data['Data']['Session'] = f"playing {game_type}:{format_name(status_data['session']['mode'])}"
            else: formatted_player_data['Data']['Session'] = "Offline"
      else: formatted_player_data['Data']['Session'] = "in Invisible Mode"
      
      if "stats" not in player_data['player'] or "Arcade" not in player_data['player']['stats']: 
            player_data['player']['stats'] = { "Arcade": {} }
      
      arcade_data: dict = player_data['player']['stats']['Arcade']
      player_zombies_data = {
            "General": {
                  "Wins": fix_key_error(arcade_data, 'wins_zombies'),
                  "TRS": fix_key_error(arcade_data, 'total_rounds_survived_zombies'),
                  "Kills": fix_key_error(arcade_data, 'zombie_kills_zombies'),
                  "Accuracy": round((fix_key_error(arcade_data, 'bullets_hit_zombies') / max(fix_key_error(arcade_data, 'bullets_shot_zombies'), 1) * 100)),
                  "Headshots": round((fix_key_error(arcade_data, 'headshots_zombies') / max(fix_key_error(arcade_data, 'bullets_hit_zombies'), 1) * 100)),
                  "K/D": round(fix_key_error(arcade_data, 'zombie_kills_zombies') / max(fix_key_error(arcade_data, 'deaths_zombies'), 1)),
                  "Revives": fix_key_error(arcade_data, 'players_revived_zombies'),
                  "Downs": fix_key_error(arcade_data, 'times_knocked_down_zombies'),
                  "Deaths": fix_key_error(arcade_data, 'deaths_zombies'),
                  "Doors": fix_key_error(arcade_data, 'doors_opened_zombies'),
                  "Windows": fix_key_error(arcade_data, 'windows_repaired_zombies'),
            },
            "Dead End": {
                  "General": {
                        "Wins": fix_key_error(arcade_data, 'wins_zombies_deadend'),
                        "Kills": fix_key_error(arcade_data, 'zombie_kills_zombies_deadend'),
                        "Revives": fix_key_error(arcade_data, 'players_revived_zombies_deadend'),
                        "Downs": fix_key_error(arcade_data, 'times_knocked_down_zombies_deadend'),
                        "Deaths": fix_key_error(arcade_data, 'deaths_zombies_deadend'),
                        "TRS": fix_key_error(arcade_data, 'total_rounds_survived_zombies_deadend'),
                        "Doors": fix_key_error(arcade_data, 'doors_opened_zombies_deadend'),
                        "Windows": fix_key_error(arcade_data, 'windows_repaired_zombies_deadend'),
                  },
                  "Normal": {
                        "Wins": fix_key_error(arcade_data, 'wins_zombies_deadend_normal'),
                        "BR": fix_key_error(arcade_data, 'best_round_zombies_deadend_normal'),
                        "FTB-R10": make_secs_readable( fix_key_error(arcade_data, 'fastest_time_10_zombies_deadend_normal')),
                        "FTB-R20": make_secs_readable( fix_key_error(arcade_data, 'fastest_time_20_zombies_deadend_normal')),
                        "FTB-R30": make_secs_readable( fix_key_error(arcade_data, 'fastest_time_30_zombies_deadend_normal')),
                        "Kills": fix_key_error(arcade_data, 'zombie_kills_zombies_deadend_normal'),
                        "Revives": fix_key_error(arcade_data, 'players_revived_zombies_deadend_normal'),
                        "Downs": fix_key_error(arcade_data, 'times_knocked_down_zombies_deadend_normal'),
                        "Deaths": fix_key_error(arcade_data, 'deaths_zombies_deadend_normal'),
                        "TRS": fix_key_error(arcade_data, 'total_rounds_survived_zombies_deadend_normal'),
                        "Doors": fix_key_error(arcade_data, 'doors_opened_zombies_deadend_normal'),
                        "Windows": fix_key_error(arcade_data, 'windows_repaired_zombies_deadend_normal'),
                  },
                  "Hard": {
                        "Wins": fix_key_error(arcade_data, 'wins_zombies_deadend_hard'),
                        "BR": fix_key_error(arcade_data, 'best_round_zombies_deadend_hard'),
                        "FTB-R10": make_secs_readable(fix_key_error(arcade_data, 'fastest_time_10_zombies_deadend_hard')),
                        "FTB-R20": make_secs_readable(fix_key_error(arcade_data, 'fastest_time_20_zombies_deadend_hard')),
                        "FTB-R30": make_secs_readable(fix_key_error(arcade_data, 'fastest_time_30_zombies_deadend_hard')),
                        "Kills": fix_key_error(arcade_data, 'zombie_kills_zombies_deadend_hard'),
                        "Revives": fix_key_error(arcade_data, 'players_revived_zombies_deadend_hard'),
                        "Downs": fix_key_error(arcade_data, 'times_knocked_down_zombies_deadend_hard'),
                        "Deaths": fix_key_error(arcade_data, 'deaths_zombies_deadend_hard'),
                        "TRS": fix_key_error(arcade_data, 'total_rounds_survived_zombies_deadend_hard'),
                        "Doors": fix_key_error(arcade_data, 'doors_opened_zombies_deadend_hard'),
                        "Windows": fix_key_error(arcade_data, 'windows_repaired_zombies_deadend_hard'),
                  },
                  "RIP": {
                        "Wins": fix_key_error(arcade_data, 'wins_zombies_deadend_rip'),
                        "BR": fix_key_error(arcade_data, 'best_round_zombies_deadend_rip'),
                        "FTB-R10": make_secs_readable(fix_key_error(arcade_data, 'fastest_time_10_zombies_deadend_rip')),
                        "FTB-R20": make_secs_readable(fix_key_error(arcade_data, 'fastest_time_20_zombies_deadend_rip')),
                        "FTB-R30": make_secs_readable(fix_key_error(arcade_data, 'fastest_time_30_zombies_deadend_rip')),
                        "Kills": fix_key_error(arcade_data, 'zombie_kills_zombies_deadend_rip'),
                        "Revives": fix_key_error(arcade_data, 'players_revived_zombies_deadend_rip'),
                        "Downs": fix_key_error(arcade_data, 'times_knocked_down_zombies_deadend_rip'),
                        "Deaths": fix_key_error(arcade_data, 'deaths_zombies_deadend_rip'),
                        "TRS": fix_key_error(arcade_data, 'total_rounds_survived_zombies_deadend_rip'),
                        "Doors": fix_key_error(arcade_data, 'doors_opened_zombies_deadend_rip'),
                        "Windows": fix_key_error(arcade_data, 'windows_repaired_zombies_deadend_rip'),
                  }
            },
            "Bad Blood": {
                  "General": {
                        "Wins": fix_key_error(arcade_data, 'wins_zombies_badblood'),
                        "Kills": fix_key_error(arcade_data, 'zombie_kills_zombies_badblood'),
                        "Revives": fix_key_error(arcade_data, 'players_revived_zombies_badblood'),
                        "Downs": fix_key_error(arcade_data, 'times_knocked_down_zombies_badblood'),
                        "Deaths": fix_key_error(arcade_data, 'deaths_zombies_badblood'),
                        "TRS": fix_key_error(arcade_data, 'total_rounds_survived_zombies_badblood'),
                        "Doors": fix_key_error(arcade_data, 'doors_opened_zombies_badblood'),
                        "Windows": fix_key_error(arcade_data, 'windows_repaired_zombies_badblood'),
                  },
                  "Normal": {
                        "Wins": fix_key_error(arcade_data, 'wins_zombies_badblood_normal'),
                        "BR": fix_key_error(arcade_data, 'best_round_zombies_badblood_normal'),
                        "FTB-R10": make_secs_readable(fix_key_error(arcade_data, 'fastest_time_10_zombies_badblood_normal')),
                        "FTB-R20": make_secs_readable(fix_key_error(arcade_data, 'fastest_time_20_zombies_badblood_normal')),
                        "FTB-R30": make_secs_readable(fix_key_error(arcade_data, 'fastest_time_30_zombies_badblood_normal')),
                        "Kills": fix_key_error(arcade_data, 'zombie_kills_zombies_badblood_normal'),
                        "Revives": fix_key_error(arcade_data, 'players_revived_zombies_badblood_normal'),
                        "Downs": fix_key_error(arcade_data, 'times_knocked_down_zombies_badblood_normal'),
                        "Deaths": fix_key_error(arcade_data, 'deaths_zombies_badblood_normal'),
                        "TRS": fix_key_error(arcade_data, 'total_rounds_survived_zombies_badblood_normal'),
                        "Doors": fix_key_error(arcade_data, 'doors_opened_zombies_badblood_normal'),
                        "Windows": fix_key_error(arcade_data, 'windows_repaired_zombies_badblood_normal'),
                  },
                  "Hard": {
                        "Wins": fix_key_error(arcade_data, 'wins_zombies_badblood_hard'),
                        "BR": fix_key_error(arcade_data, 'best_round_zombies_badblood_hard'),
                        "FTB-R10": make_secs_readable(fix_key_error(arcade_data, 'fastest_time_10_zombies_badblood_hard')),
                        "FTB-R20": make_secs_readable(fix_key_error(arcade_data, 'fastest_time_20_zombies_badblood_hard')),
                        "FTB-R30":make_secs_readable(fix_key_error(arcade_data, 'fastest_time_30_zombies_badblood_hard')),
                        "Kills": fix_key_error(arcade_data, 'zombie_kills_zombies_badblood_hard'),
                        "Revives": fix_key_error(arcade_data, 'players_revived_zombies_badblood_hard'),
                        "Downs": fix_key_error(arcade_data, 'times_knocked_down_zombies_badblood_hard'),
                        "Deaths": fix_key_error(arcade_data, 'deaths_zombies_badblood_hard'),
                        "TRS": fix_key_error(arcade_data, 'total_rounds_survived_zombies_badblood_hard'),
                        "Doors": fix_key_error(arcade_data, 'doors_opened_zombies_badblood_hard'),
                        "Windows": fix_key_error(arcade_data, 'windows_repaired_zombies_badblood_hard'),
                  },
                  "RIP": {
                        "Wins": fix_key_error(arcade_data, 'wins_zombies_badblood_rip'),
                        "BR": fix_key_error(arcade_data, 'best_round_zombies_badblood_rip'),
                        "FTB-R10": make_secs_readable(fix_key_error(arcade_data, 'fastest_time_10_zombies_badblood_rip')),
                        "FTB-R20": make_secs_readable(fix_key_error(arcade_data, 'fastest_time_20_zombies_badblood_rip')),
                        "FTB-R30": make_secs_readable(fix_key_error(arcade_data, 'fastest_time_30_zombies_badblood_rip')),
                        "Kills": fix_key_error(arcade_data, 'zombie_kills_zombies_badblood_rip'),
                        "Revives": fix_key_error(arcade_data, 'players_revived_zombies_badblood_rip'),
                        "Downs": fix_key_error(arcade_data, 'times_knocked_down_zombies_badblood_rip'),
                        "Deaths": fix_key_error(arcade_data, 'deaths_zombies_badblood_rip'),
                        "TRS": fix_key_error(arcade_data, 'total_rounds_survived_zombies_badblood_rip'),
                        "Doors": fix_key_error(arcade_data, 'doors_opened_zombies_badblood_rip'),
                        "Windows": fix_key_error(arcade_data, 'windows_repaired_zombies_badblood_rip'),
                  }
            },
            "Alien Arcadium": {
                  "Wins": fix_key_error(arcade_data, 'wins_zombies_alienarcadium_normal'),
                  "BR": fix_key_error(arcade_data, 'best_round_zombies_alienarcadium'),
                  "FTB-R10": make_secs_readable(fix_key_error(arcade_data, 'fastest_time_10_zombies_alienarcadium_normal')),
                  "FTB-R20": make_secs_readable(fix_key_error(arcade_data, 'fastest_time_20_zombies_alienarcadium_normal')),
                  "Kills": fix_key_error(arcade_data, 'zombie_kills_zombies_alienarcadium'),
                  "Revives": fix_key_error(arcade_data, 'players_revived_zombies_alienarcadium'),
                  "Downs": fix_key_error(arcade_data, 'times_knocked_down_zombies_alienarcadium'),
                  "Deaths": fix_key_error(arcade_data, 'deaths_zombies_alienarcadium'),
                  "TRS": fix_key_error(arcade_data, 'total_rounds_survived_zombies_alienarcadium'),
                  "Doors": fix_key_error(arcade_data, 'doors_opened_zombies_alienarcadium'),
                  "Windows": fix_key_error(arcade_data, 'windows_repaired_zombies_alienarcadium')
            }
      }
      
      formatted_player_data["Data"]["Zombies"] = player_zombies_data
      return formatted_player_data


def make_secs_readable(timer: int):
      if timer < 3600: return f"{str(math.floor(timer / 60)).zfill(2)}:{str(math.floor((timer % 60))).zfill(2)}"
      else: return f"{math.floor(timer / 3600)}:{str(math.floor((timer % 3600) / 60)).zfill(2)}:{str(math.floor((timer % 60))).zfill(2)}"


def guild_level(exp):
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
      else: return (exp - 15000000) // 3000000 + 12


def fix_key_error(stats: dict, key: str):
      try: return stats[key]
      except KeyError: return 0
 
 
def fix_rank_title(stats: dict, key: str) -> str:
      if key in stats:
            rank = stats[key].replace("_PLUS", "+")
            if "monthlyPackageRank" in stats and stats['monthlyPackageRank'] != "NONE": rank = "MVP++"
            return f"[{rank}] "
      return ""


def format_lanauge(stats: dict, key: str):
      if key in stats: return format_name(stats[key])
      return "Unspecified"


def format_name(name: str):
    words = name.split('_')
    formatted_words = [word.capitalize() for word in words] # Capitalize the first character of each word and lowercase the rest
    formatted_game_type = ' '.join(formatted_words)
    return formatted_game_type