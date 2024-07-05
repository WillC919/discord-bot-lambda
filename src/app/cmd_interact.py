import find_cmd
import help_cmd


def echo(data) -> dict:
    original_message = data["options"][0]["value"]    
    embed = {
        "title": "Poly the parrot",
        "description": f"Echo: {original_message}",
        "color": 0x5865F2,  # Blurple color
        "thumbnail": { "url": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/d/de/Red_Parrot.png/revision/latest?cb=20170720112713" },
    }
    return { "embeds": [embed] }


def help(data):
    embed = {}
    if "options" in data and data["options"]: embed = help_cmd.make_help_embed(data["options"][0]["value"])
    else: embed = help_cmd.make_help_embed()
    return { "embeds": [embed] }


def find(table, username: str, args: list[str], edit: bool):
    if edit: response = find_cmd.get_player_data_from_aws_db(table, username, args)
    else: response = find_cmd.get_player_data(table, username)
    return_data = { "embeds": [response[1]] }
    
    if not response[0]: return return_data # Error occured
    
    # Buttons Section
    g_button = { "type": 2, "style": 2, "label": "<<", "custom_id": f"find-{username}-g" }
    de_button = { "type": 2, "style": 1, "label": "Dead End", "custom_id": f"find-{username}-de-g" }
    bb_button = { "type": 2, "style": 1, "label": "Bad Blood", "custom_id": f"find-{username}-bb-g" }
    aa_button = { "type": 2, "style": 1, "label": "Alien Arcadium", "custom_id": f"find-{username}-aa" }
    p_button = { "type": 2, "style": 1, "label": "Prison", "custom_id": f"find-{username}-p-g" }
    
    if not edit or args[0] == "g":
        return_data["components"] = [ { "type": 1, "components": [de_button, bb_button, aa_button, p_button] } ]
    elif args[0] == "aa":
        return_data["components"] = [ { "type": 1, "components": [g_button] } ]
    else:
        gen_button = { "type": 2, "style": 2, "label": "<<", "custom_id": f"find-{username}-{args[0]}-g" }
        norm_button = { "type": 2, "style": 1, "label": "Normal", "custom_id": f"find-{username}-{args[0]}-n" }
        hard_button = { "type": 2, "style": 1, "label": "Hard", "custom_id": f"find-{username}-{args[0]}-h" }
        rip_button = { "type": 2, "style": 1, "label": "RIP", "custom_id": f"find-{username}-{args[0]}-r" }
        
        norm_button["disabled"] = False
        hard_button["disabled"] = False
        rip_button["disabled"] = False
        
        if args[1] == 'g':
            return_data["components"] = [ { "type": 1, "components": [g_button, norm_button, hard_button, rip_button] } ]
        if args[1] == 'n':
            norm_button["disabled"] = True
            return_data["components"] = [ { "type": 1, "components": [gen_button, norm_button, hard_button, rip_button] } ]
        if args[1] == 'h':
            hard_button["disabled"] = True
            return_data["components"] = [ { "type": 1, "components": [gen_button, norm_button, hard_button, rip_button] } ]
        if args[1] == 'r':
            rip_button["disabled"] = True
            return_data["components"] = [ { "type": 1, "components": [gen_button, norm_button, hard_button, rip_button] } ]
        
    return return_data