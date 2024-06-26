def make_help_embed(command: str = None):
    embed = {}
    if not command:
        embed = {
            "title": "List of commands",
            "description": "To get additional information about specific commands type /help [command_name]",
            "color": 0x5865F2,  # Blurple color
            "thumbnail": {
                "url": "https://art.pixilart.com/0c935a31c866469.png"
            },
            "fields": [
                {"name": "- echo\t\t\t\t\t\t   ‎", "value": "", "inline": True},
                {"name": "- find\t\t\t\t\t\t   ‎", "value": "", "inline": True},
                {"name": "- help\t\t\t\t\t\t   ‎", "value": "", "inline": True}
            ]
        }

    elif command == "find":
        embed = {
            "title": "/find commands",
            "description": "Looks up on player's zombies stats based on given arguments\n"
                            "`/find [map] [mode] [username_1] ... [up_to_username_4]`\n"
                            "First 3 arguments are required to be filled and all arguments are NOT case sensitive\n\n"
                            
                            "**Map Arguments:\n**"
                            "- General\n"
                            "`[g | gen | general | s | sum | summary]`\n"
                            "- Dead End\n"
                            "`[de | dead end | dead_end]`\n"
                            "- Bad Blood\n"
                            "`[bb | bad blood | bad_blood]`\n"
                            "- Alien arcadium"
                            "`[aa | arcadium | alien arcadium | alien_arcadium]`\n\n"
                
                            "**Mode Arguments: only applicable Dead End and Bad Blood maps\n**"
                            "- General\n"
                            "`[g | gen | general | s | sum | summary]`\n"
                            "- Normal\n" 
                            "`[n | norm | normal]`\n"
                            "- Hard\n" 
                            "`[h | hard]`\n"
                            "- RIP\n"
                            "`[r | rip]`\n"
                            "- All\n"
                            "`[a | all]`",
            "color": 0x5865F2,  # Blurple color
        }
    else:
        embed = {
            "title": "Does Not Exist",
            "description": "The command you are looking for does not exist\n",
            "color": 0x8f0028,  # Darkredish color
        }
    return embed