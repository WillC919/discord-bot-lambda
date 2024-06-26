SKIN_LINK = "https://api.mineatar.io/body/full/"


def make_player_data_embed_base(player_data: dict, player_name: str, map: str, mode: str):
    # retrieveCache = False
    if not player_data['success']:
        if player_data['cause'] == "You have already looked up this name recently":
            # retrieveCache = True
            # player_data = storage.getTheCacheData(player_name)
            # if player_data == "No Match" or player_data == "No Cache":
            return make_error_embed(501, f"**{reformat_username(player_name)}**'s dataset found but unable to retrieve it. Try again in 1 min!")
        elif player_data['cause'] == "Player data does not exist":
            return make_error_embed(201, f"**{reformat_username(player_name)}** does not exist in Hypixel's Databases!")
        elif player_data['cause'] == "Invalid API key":
            return make_error_embed(403, "Current API Key is invalid. A new API Key is required!")
        elif player_data['cause'] == "Key throttle":
            return make_error_embed(429, "Maximum number of API requests has been exceeded! Try again in 5 mins!")
        else:
            return make_error_embed(900, "Unknown Error:" + player_data['cause'])
    
    formatted_args = format_args(map, mode)
    if not formatted_args: 
        return make_error_embed(901, "Please specify a valid map and/or mode")
    
    return make_player_data_embed(player_data["Data"], formatted_args[0], formatted_args[1], formatted_args[2])


def make_player_data_embed(player_data: dict, map: str, mode: list, colors: list):
    if map not in player_data['Zombies']: return [make_error_embed(801, "Please specify a valid map")]
    
    player_map_data = player_data['Zombies'][map]
    embed_data = []
    
    if map == "General":
        embed_data = [{
            "title": f"{player_data['Rank']}{reformat_username(player_data['Name'])}",
            "description": "General Statistics",
            "color": 0x9C9C9C,  # Hex color code for lighter gray
            "thumbnail": { "url": f"{SKIN_LINK}{player_data['UUID']}" },
            "fields": [
                {"name": "\nNetwork Statistics", "value": ""},
                {"name": "Level\t\t\t\t\t‎ㅤㅤ", "value": f"```{format(player_data['Network Level'], ',')}```", "inline": True},
                {"name": "Achievement Points‎", "value": f"```{format(player_data['Achievement Points'], ',')}```", "inline": True},
                {"name": "Language\t\t\t\t\t‎", "value": f"```{player_data['Language']}```", "inline": True},
                
                {"name": "\nPlayer's Guild", "value": ""},
                {"name": "Guild Name\t\t\t\t\t\t\t‎ㅤㅤ", "value": f"```{player_data['Guild']['Name'] if player_data['Guild'] else 'N/A'}```", "inline": True},
                {"name": "Level | Members\t‎ㅤㅤ", "value": f"```{format(player_data['Guild']['Level'], ',') if player_data['Guild'] else 'N/A'} | {format(player_data['Guild']['Members'], ',') if player_data['Guild'] else 'N/A'}```", "inline": True},

                {"name": "\nZombies Statistics", "value": f""},
                {"name": "Grade Score\t\t‎ㅤㅤ", "value": "```WIP```", "inline": True},
                {"name": "Wins\t\t\t\t\t\t\t\t‎", "value": f"```{format(player_map_data['Wins'], ',')}```", "inline": True},
                {"name": "Total Rounds Surv.\t‎", "value": f"```{format(player_map_data['TRS'], ',')}```", "inline": True},
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
		        "text": f"Currently {player_data['Session']}",
		        "icon_url": f"{'https://icones.pro/wp-content/uploads/2022/06/icone-du-bouton-en-ligne-vert.png' if 'playing' in player_data['Session'] else 'https://www.clker.com/cliparts/h/8/f/t/N/a/deep-red-square-md.png'}",
	        },
        }]
    elif map == "Dead End" or map == "Bad Blood":
        if mode[0] == "General":
            embed_data = [{
                "title": f"{player_data['Rank']}{reformat_username(player_data['Name'])}",
                "description": f"General {map} Zombies Statistics",
                "color": 0x008080 if map == "Dead End" else 0x8B0000,  # Dark teal for "Dead End", dark red otherwise
                "thumbnail": { "url": f"{SKIN_LINK}{player_data['UUID']}" },
                "fields": [
                    {"name": "Grade Score\t\t\t\t\t ‎", "value": "```WIP```", "inline": True},
                    {"name": "Wins\t\t\t\t\t\t\t\t   ‎", "value": f"```{format(player_map_data['General']['Wins'], ',')}```", "inline": True},
                    {"name": "Total Rounds Survived ‎", "value": f"```{format(player_map_data['General']['TRS'], ',')}```", "inline": True},
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
		            "text": f"Currently {player_data['Session']}",
		            "icon_url": f"{'https://icones.pro/wp-content/uploads/2022/06/icone-du-bouton-en-ligne-vert.png' if 'playing' in player_data['Session'] else 'https://www.clker.com/cliparts/h/8/f/t/N/a/deep-red-square-md.png'}",
	            },
            }]
        else:
            for i in range(len(mode)):
                m: str = mode[i]     
                embed = {
                    "title": f"{player_data['Rank']}{reformat_username(player_data['Name'])}",
                    "description": f"[{m}] {map} Zombies Statistics",
                    "color": colors[i],
                    "thumbnail": { "url": f"{SKIN_LINK}{player_data['UUID']}"},
                    "fields": [
                        {"name": "Wins\t\t\t\t\t\t\t\t   ‎", "value": f"```{format(player_map_data[m]['Wins'], ',')}```", "inline": True},
                        {"name": "Best Rounds\t\t\t\t\t ‎", "value": f"```{player_map_data[m]['BR']}```", "inline": True},
                        {"name": "Total Rounds Survived ‎", "value": f"```{format(player_map_data[m]['TRS'], ',')}```", "inline": True},
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
		                "text": f"Currently {player_data['Session']}",
		                "icon_url": f"{'https://icones.pro/wp-content/uploads/2022/06/icone-du-bouton-en-ligne-vert.png' if 'playing' in player_data['Session'] else 'https://www.clker.com/cliparts/h/8/f/t/N/a/deep-red-square-md.png'}",
	                },
                }
                embed_data.append(embed)
    elif map == "Alien Arcadium":
        embed_data = [{
            "title": f"{player_data['Rank']}{reformat_username(player_data['Name'])}",
            "description": "Alien Arcadium Zombies Statistics",
            "color": 0x5865F2,  # Blurple color
            "thumbnail": { "url": f"{SKIN_LINK}{player_data['UUID']}"},
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
                "text": f"Currently {player_data['Session']}",
                "icon_url": f"{'https://icones.pro/wp-content/uploads/2022/06/icone-du-bouton-en-ligne-vert.png' if 'playing' in player_data['Session'] else 'https://www.clker.com/cliparts/h/8/f/t/N/a/deep-red-square-md.png'}",
            },
        }]
    else: return [make_error_embed(802, "Please specify a valid map")]
    return embed_data


def format_args(map: str, mode: str):
    formatted_args = ["", [], []]
    if not map: 
        return None

    map = map.lower()
    if map == "g" or map == "gen" or map == "general" or map == "s" or map == "sum" or map == "summary": 
        formatted_args[0] = "General"
        return formatted_args
    elif map == "de" or map == "dead end" or map == "dead_end": 
        formatted_args[0] = "Dead End"
    elif map == "bb" or map == "bad blood" or map == "dead_end": 
        formatted_args[0] = "Bad Blood"
    elif map == "aa" or map == "arcadium" or map == "alien arcadium" or map == "alien_arcadium": 
        formatted_args[0] = "Alien Arcadium"
        return formatted_args
    else: 
        return None

    if not mode or formatted_args[0] == "General" or formatted_args[0] == "Alien Arcadium": 
        formatted_args[1] = "General"
    else:
        mode = mode.lower()
        if mode == "g" or mode == "gen" or mode == "general" or mode == "s" or mode == "sum" or mode == "summary":
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