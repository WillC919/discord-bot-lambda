# SKIN_LINK = "https://api.mineatar.io/body/full/"
SKIN_LINK = "https://starlightskins.lunareclipse.studio/render/walking/" # Visit https://docs.lunareclipse.studio/ for documentation
ONLINE_LINK = "https://www.clker.com/cliparts/L/u/0/1/d/C/green-square-md.png"
OFFLINE_LINK = "https://www.clker.com/cliparts/h/8/f/t/N/a/deep-red-square-md.png"


def make_player_data_embed_base(table, player_data: dict, player_name: str, formatted_args: list):
    cache_retrieved_recently = False
    username = player_name.lower()
    
    if not player_data['success']:
        if player_data['cause'] == "You have already looked up this name recently":
            response = table.get_item(Key={"player_name": username})
            if "Item" not in response:
                return make_error_embed(501, f"**{reformat_username(player_name)}**'s dataset was found but unable to retrieve it. Try again in 1 minute!")
            player_data = response["Item"]["cache_data"]
            cache_retrieved_recently = True
        elif player_data['cause'] == "Player data does not exist":
            return make_error_embed(201, f"**{reformat_username(player_name)}** does not exist in Hypixel's Databases!")
        elif player_data['cause'] == "Invalid API key":
            return make_error_embed(403, "The current API Key is invalid. A new API Key is required!")
        elif player_data['cause'] == "Key throttle":
            return make_error_embed(429, "The number of API requests exceeded the threshold! Try again in 5 mins!")
        else: return make_error_embed(900, "Unknown Error:" + player_data['cause'])
    
    if not cache_retrieved_recently:
        if table.item_count >= 64:
            scan = table.scan()
            with table.batch_writer() as batch:
                for each in scan['Items']:
                    batch.delete_item(Key={'player_name': each['player_name']})
                    
        table.put_item(Item={"player_name": username, "cache_data": player_data})
    return make_player_data_embed(player_data["Data"], formatted_args[0], formatted_args[1], formatted_args[2])


def make_player_data_embed(player_data: dict, map: str, mode: list, colors: list):
    if map not in player_data['Zombies']: return [make_error_embed(801, "Please specify a valid map")]
    
    player_map_data = player_data['Zombies'][map]
    skin_link = f"{SKIN_LINK}{player_data['UUID']}/full"
    session_img_link = OFFLINE_LINK if player_data['Session'] == "Offline" or player_data['Session'] == "in Invisible Mode" else ONLINE_LINK
    session_text = f"Currently {player_data['Session']}\nBot is NOT affiliated or endorsed by Hypixel"
    
    embed_data = []
    if map == "General":
        embed_data = [{
            "title": f"{player_data['Rank']}{reformat_username(player_data['Name'])}",
            "description": "General Statistics",
            "color": 0x9C9C9C,  # Hex color code for lighter gray
            "thumbnail": { "url": skin_link },
            "fields": [
                {"name": "\nNetwork Statistics", "value": ""},
                {"name": "Level\t\t\t\t\t‎", "value": f"```{format(player_data['Network Level'], ',')}```", "inline": True},
                {"name": "Achievement Points‎", "value": f"```{format(player_data['Achievement Points'], ',')}```", "inline": True},
                {"name": "Language\t\t\t\t\t‎", "value": f"```{player_data['Language']}```", "inline": True},    
                {"name": "", "value": ""},
                {"name": f"Guild Name {'- lvl. ' + format(player_data['Guild']['Level'], ',') if player_data['Guild'] else ''}\t\t‎", "value": f"```{player_data['Guild']['Name'] if player_data['Guild'] else 'N/A'}```", "inline": True},
                {"name": "Members\t‎", "value": f"```{format(player_data['Guild']['Members'], ',') if player_data['Guild'] else 'N/A'}```", "inline": True},

                {"name": "‎", "value": ""},
                {"name": "\nZombies Statistics", "value": f""},
                {"name": "Grade Score\t‎", "value": "```WIP```", "inline": True},
                {"name": "Wins\t\t\t\t\t\t‎", "value": f"```{format(player_map_data['Wins'], ',')}```", "inline": True},
                {"name": "Total Rounds Surv.‎", "value": f"```{format(player_map_data['TRS'], ',')}```", "inline": True},
                {"name": "Hit Accuracy", "value": f"```{player_map_data['Accuracy']}%```", "inline": True},
                {"name": "Headshots Accuracy", "value": f"```{player_map_data['Headshots']}%```", "inline": True},
                {"name": "Kill/Death Ratio", "value": f"```{format(player_map_data['K/D'], ',')}```", "inline": True},
                {"name": "Kills", "value": f"```{format(player_map_data['Kills'], ',')}```", "inline": True},
                {"name": "Downs", "value": f"```{format(player_map_data['Downs'], ',')}```", "inline": True},
                {"name": "Deaths", "value": f"```{format(player_map_data['Deaths'], ',')}```", "inline": True},
                {"name": "Revives", "value": f"```{format(player_map_data['Revives'], ',')}```", "inline": True},
                {"name": "Doors Opened", "value": f"```{format(player_map_data['Doors'], ',')}```", "inline": True},
                {"name": "Windows Repaired", "value": f"```{format(player_map_data['Windows'], ',')}```", "inline": True},
            ],
            "footer": {
		        "text": session_text,
		        "icon_url": session_img_link,
	        },
        }]
    elif map == "Dead End" or map == "Bad Blood" or map == "Prison":
        if mode[0] == "General":
            embed_colors = { "Dead End": 0x008080, "Bad Blood": 0x8B0000, "Prison": 0x8B7000 }
            embed_data = [{
                "title": f"{player_data['Rank']}{reformat_username(player_data['Name'])}",
                "description": f"General {map} Zombies Statistics",
                "color": embed_colors[map],  # Dark teal for "Dead End", dark red otherwise
                "thumbnail": { "url": skin_link },
                "fields": [
                    {"name": "Grade Score\t\t‎ㅤㅤ", "value": "```WIP```", "inline": True},
                    {"name": "Wins\t\t\t\t\t\t\t\t‎", "value": f"```{format(player_map_data['General']['Wins'], ',')}```", "inline": True},
                    {"name": "Total Rounds Surv.\t‎", "value": f"```{format(player_map_data['General']['TRS'], ',')}```", "inline": True},
                    {"name": "Normal Best Rounds", "value": f"```{player_map_data['Normal']['BR']}```", "inline": True},
                    {"name": "Hard Best Rounds", "value": f"```{player_map_data['Hard']['BR']}```", "inline": True},
                    {"name": "RIP Best Rounds", "value": f"```{player_map_data['RIP']['BR']}```", "inline": True},
                    {"name": "Normal FTB R30", "value": f"```{player_map_data['Normal']['FTB-R30']}```", "inline": True},
                    {"name": "Hard FTB R30", "value": f"```{player_map_data['Hard']['FTB-R30']}```", "inline": True},
                    {"name": "RIP FTB R30", "value": f"```{player_map_data['RIP']['FTB-R30']}```", "inline": True},
                    {"name": "Kills", "value": f"```{format(player_map_data['General']['Kills'], ',')}```", "inline": True},
                    {"name": "Deaths", "value": f"```{format(player_map_data['General']['Deaths'], ',')}```", "inline": True},
                    {"name": "Revives", "value": f"```{format(player_map_data['General']['Revives'], ',')}```", "inline": True},
                ],
                "footer": {
		            "text": session_text,
		            "icon_url": session_img_link,
	            },
            }]
        else:
            for i in range(len(mode)):
                m: str = mode[i]     
                embed = {
                    "title": f"{player_data['Rank']}{reformat_username(player_data['Name'])}",
                    "description": f"[{m}] {map} Zombies Statistics",
                    "color": colors[i],
                    "thumbnail": { "url": skin_link },
                    "fields": [
                        {"name": "Wins\t\t\t\t\t\t\t\t‎", "value": f"```{format(player_map_data[m]['Wins'], ',')}```", "inline": True},
                        {"name": "Best Rounds\t\t\t\t‎", "value": f"```{player_map_data[m]['BR']}```", "inline": True},
                        {"name": "Total Rounds Surv.\t‎", "value": f"```{format(player_map_data[m]['TRS'], ',')}```", "inline": True},
                        {"name": "Fastest Time by R10", "value": f"```{player_map_data[m]['FTB-R10']}```", "inline": True},
                        {"name": "Fastest Time by R20", "value": f"```{player_map_data[m]['FTB-R20']}```", "inline": True},
                        {"name": "Fastest Time by R30", "value": f"```{player_map_data[m]['FTB-R30']}```", "inline": True},
                        {"name": "Kills", "value": f"```{format(player_map_data[m]['Kills'], ',')}```", "inline": True},
                        {"name": "Downs", "value": f"```{format(player_map_data[m]['Downs'], ',')}```", "inline": True},
                        {"name": "Deaths", "value": f"```{format(player_map_data[m]['Deaths'], ',')}```", "inline": True},
                        {"name": "Revives", "value": f"```{format(player_map_data[m]['Revives'], ',')}```", "inline": True},
                        {"name": "Doors Opened", "value": f"```{format(player_map_data[m]['Doors'], ',')}```", "inline": True},
                        {"name": "Windows Repaired", "value": f"```{format(player_map_data[m]['Windows'], ',')}```", "inline": True}
                    ],
                    "footer": {
		                "text": session_text,
		                "icon_url": session_img_link,
	                },
                }
                embed_data.append(embed)
    elif map == "Alien Arcadium":
        embed_data = [{
            "title": f"{player_data['Rank']}{reformat_username(player_data['Name'])}",
            "description": "Alien Arcadium Zombies Statistics",
            "color": 0x5865F2,  # Blurple color
            "thumbnail": { "url": skin_link },
            "fields": [
                {"name": "Grade Score\t\t\t\t\t ‎", "value": "```WIP```", "inline": True},
                {"name": "Wins\t\t\t\t\t\t\t\t   ‎", "value": f"```{format(player_map_data['Wins'], ',')}```", "inline": True},
                {"name": "Best Rounds\t\t\t\t\t ‎", "value": f"```{player_map_data['BR']}```", "inline": True},
                {"name": "Total Rounds Survived", "value": f"```{format(player_map_data['TRS'], ',')}```", "inline": True},
                {"name": "Fastest Time by R10", "value": f"```{player_map_data['FTB-R10']}```", "inline": True},
                {"name": "Fastest Time by R20", "value": f"```{player_map_data['FTB-R20']}```", "inline": True},
                {"name": "Kills", "value": f"```{format(player_map_data['Kills'], ',')}```", "inline": True},
                {"name": "Downs", "value": f"```{format(player_map_data['Downs'], ',')}```", "inline": True},
                {"name": "Deaths", "value": f"```{format(player_map_data['Deaths'], ',')}```", "inline": True},
                {"name": "Revives", "value": f"```{format(player_map_data['Revives'], ',')}```", "inline": True},
                {"name": "Doors Opened", "value": f"```{format(player_map_data['Doors'], ',')}```", "inline": True},
                {"name": "Windows Repaired", "value": f"```{format(player_map_data['Windows'], ',')}```", "inline": True},
            ],
            "footer": {
                "text": session_text,
                "icon_url": session_img_link,
            },
        }]
    else: return [make_error_embed(802, "Please specify a valid map")]
    return embed_data


def format_args(map: str, mode: str):
    formatted_args = ["", [], []]
    if not map: 
        return None

    map = map.lower()
    if map == "g" or map == "gen" or map == "general": 
        formatted_args[0] = "General"
        return formatted_args
    elif map == "de" or map == "dead end" or map == "dead_end": 
        formatted_args[0] = "Dead End"
    elif map == "bb" or map == "bad blood" or map == "dead_end": 
        formatted_args[0] = "Bad Blood"
    elif map == "p" or map == "pr" or map == "prison": 
        formatted_args[0] = "Prison"
    elif map == "aa" or map == "arcadium" or map == "alien arcadium" or map == "alien_arcadium": 
        formatted_args[0] = "Alien Arcadium"
        return formatted_args
    else: 
        return None

    if not mode or formatted_args[0] == "General" or formatted_args[0] == "Alien Arcadium": 
        formatted_args[1] = "General"
    else:
        mode = mode.lower()
        if mode == "g" or mode == "gen" or mode == "general":
            formatted_args[1] = ["General"]
            formatted_args[2] = [0x000000]
        elif mode == "n" or mode == "normal":
            formatted_args[1] = ["Normal"]
            formatted_args[2] = [0x1DB954]
        elif mode == "h" or mode == "hard":
            formatted_args[1] = ["Hard"] 
            formatted_args[2] = [0xAEC202]
        elif mode == "r" or mode == "rip":
            formatted_args[1] = ["RIP"]
            formatted_args[2] = [0xC20202]
        elif mode == "a" or mode == "all":
            formatted_args[1] = ['Normal', 'Hard', 'RIP']
            formatted_args[2] = [0x1DB954, 0xAEC202, 0xC20202]
        else: 
            return None
        
    return formatted_args


def make_error_embed(num: int = 0, error_msg: str = ""):
    embed = {
        "title": f"❌ ERROR {num}",
        "description": error_msg,
        "color": 0xFF0000  # Red color
    }
    return embed


def reformat_username(name: str):
    reformatted_name = ""
    for i in range(len(name)):
        if name[i] == "_":
            reformatted_name += "\_"
        else:
            reformatted_name += name[i]
    return reformatted_name