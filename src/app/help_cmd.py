def make_help_embed(command: str = None):
    embed = {}
    if not command:
        embed = {
            "title": "List of commands",
            "description": "To get additional information about specific commands type /help [command_name].",
            "color": 0x5865F2,  # Blurple color
            "thumbnail": {
                "url": "https://art.pixilart.com/0c935a31c866469.png"
            },
            "fields": [
                {"name": "/echo\t\t\t\t\t\t   ‎", "value": "", "inline": True},
                {"name": "/find\t\t\t\t\t\t   ‎", "value": "", "inline": True},
                {"name": "/help\t\t\t\t\t\t   ‎", "value": "", "inline": True}
            ],
            "footer": { "text": "Bot is NOT affiliated or endorsed by Hypixel" },
        }
    elif command == "find":
        embed = {
            "title": "/find command",
            "color": 0x5865F2,  # Blurple color
            "description": "Looks up the player's Zombies stats based on given arguments.\n"
                            "`/find [map] [mode] [username_1] [username_2] [username_3]`\n"
                            "The last 2 arguments are optional. All arguments are NOT case-sensitive.\n\n",
            "fields": [
                {"name": "Map Arguments:", "value": ""},
                {"name": "General", "value": "`[g | gen | general]`", "inline": True},
                {"name": "Dead End", "value": "`[de | dead end | dead_end]`", "inline": True},
                {"name": "", "value": ""},
                {"name": "Bad Blood", "value": "`[bb | bad blood | bad_blood]`", "inline": True},
                {"name": "Alien arcadium", "value": "`[aa | arcadium | alien arcadium | alien_arcadium]`", "inline": True},
                {"name": "", "value": ""},
                {"name": "Prison", "value": "`[p | pr | prison]`", "inline": True},
                
                {"name": "Mode Arguments:", "value": ""},
                {"name": "General", "value": "`[g | gen | general]`", "inline": True},
                {"name": "Normal", "value": "`[n | norm | normal]`", "inline": True},
                {"name": "", "value": ""},
                {"name": "Hard", "value": "`[h | hard]`", "inline": True},
                {"name": "RIP", "value": "`[r | rip]`", "inline": True},
                {"name": "", "value": ""},
                {"name": "Bad Blood", "value": "`[bb | bad blood | bad_blood]`", "inline": True},
            ],
            "footer": { "text": "Bot is NOT affiliated or endorsed by Hypixel" },
        }
    elif command == "help":
        embed = {
            "title": "/help command",
            "color": 0x5865F2,  # Blurple color
            "description": "Provides a list of commands or additional information on specified commands.\n"
                            "`/help [command_name]`\n",
            "footer": { "text": "Bot is NOT affiliated or endorsed by Hypixel" },
        }
    elif command == "echo":
        embed = {
            "title": "/echo command",
            "color": 0x5865F2,  # Blurple color
            "description": "Echos back inputted message from server/ mainly used for testing by developer.\n"
                            "`/help [command_name]`\n",
            "footer": { "text": "Bot is NOT affiliated or endorsed by Hypixel" },
        }
    else:
        embed = {
            "title": "Does Not Exist",
            "description": "The command you are looking for does not exist\n",
            "color": 0x8f0028,  # Darkredish color
            "footer": { "text": "Bot is NOT affiliated or endorsed by Hypixel" },
        }
    return embed