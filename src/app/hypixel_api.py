import os
import requests
import math


HYPIXEL_API_KEY = os.environ.get("HYPIXEL_API_KEY")
HYPIXEL_API_LINK = f'https://api.hypixel.net/player?key={HYPIXEL_API_KEY}&name='


def get_player_data(username: str):
      player_data = (requests.get(f'{HYPIXEL_API_LINK}{username}')).json()

      if not player_data['success']:
            return player_data
      if player_data['player'] is None:
            player_data = { "success": False, "cause": "Player Data Does Not Exist" }
            return player_data
      if "stats" not in player_data['player'] or "Arcade" not in player_data['player']['stats']:
            player_data = { "success": False, "cause": "Player Data Does Not Exist" }
            return player_data
      
      
      formatted_player_data = {
            "success": True,
            "Data": {
                  "Name": player_data['player']['displayname'], 
                  "UUID": player_data['player']['uuid'], 
            }
      }
      
      arcade_data: dict = player_data['player']['stats']['Arcade']
      divsor_a = max(fix_key_error(arcade_data, 'bullets_shot_zombies'), 1)
      divsor_b = max(fix_key_error(arcade_data, 'bullets_hit_zombies'), 1)
      divsor_c = max(fix_key_error(arcade_data, 'deaths_zombies'), 1)
      
      player_zombies_data = {
            "General": {
                  "Wins": fix_key_error(arcade_data, 'wins_zombies'),
                  "TRS": fix_key_error(arcade_data, 'total_rounds_survived_zombies'),
                  "Kills": fix_key_error(arcade_data, 'zombie_kills_zombies'),
                  "Accuracy": round((fix_key_error(arcade_data, 'bullets_hit_zombies') / divsor_a * 100)),
                  "Headshots": round((fix_key_error(arcade_data, 'headshots_zombies') / divsor_b * 100)),
                  "K/D": round(fix_key_error(arcade_data, 'zombie_kills_zombies') / divsor_c),
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


def fix_key_error(stats: dict, key: str):
      try: return stats[key]
      except KeyError: return 0