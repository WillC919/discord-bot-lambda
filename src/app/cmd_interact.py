import hypixel_api
import find_cmd
import help_cmd

def echo(data) -> dict:
    original_message = data["options"][0]["value"]    
    embed = {
        "title": "Poly the parrot",
        "description": f"Echo: {original_message}",
        "color": 0x5865F2,  # Blurple color
        "thumbnail": {
            "url": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/d/de/Red_Parrot.png/revision/latest?cb=20170720112713"
        },
    }
    return { "embeds": [embed] }


def help(data):
    embed = {}
    if "options" in data and data["options"]: embed = help_cmd.make_help_embed(data["options"][0]["value"])
    else: embed = help_cmd.make_help_embed()
    return { "embeds": [embed] }


def find(table, map: str, mode: str, username: str, edit: bool):
    formatted_args = find_cmd.format_args(map, mode)
    embeds = []
    
    if not formatted_args:  embeds = [find_cmd.make_error_embed(901, "Please specify a valid map and/or mode")]
    else:
        player_data = hypixel_api.get_player_data(username)
        embed_list = find_cmd.make_player_data_embed_base(table, player_data, username, formatted_args)
        
        for embed in embed_list: 
            embeds.append(embed)
            
    return_data = { "embeds": embeds }
    de_button = { "type": 2, "style": 1, "label": "Dead End", "custom_id": f"find-de-g-{username}" }
    bb_button = { "type": 2, "style": 1, "label": "Bad Blood", "custom_id": f"find-bb-g-{username}" }
    aa_button = { "type": 2, "style": 1, "label": "Alien Arcadium", "custom_id": f"find-aa-g-{username}" }
    p_button = { "type": 2, "style": 1, "label": "Prison", "custom_id": f"find-p-g-{username}" }
    
    if formatted_args[0] == "General":
        return_data["components"] = [ { "type": 1, "components": [de_button, bb_button, aa_button, p_button] } ]
    elif edit:
        de_button["disabled"] = True
        bb_button["disabled"] = True
        aa_button["disabled"] = True
        p_button["disabled"] = True
        return_data["components"] = [ { "type": 1, "components": [de_button, bb_button, aa_button, p_button] } ]
        
    return return_data