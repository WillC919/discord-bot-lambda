import os
from flask import Flask, jsonify, request
from mangum import Mangum
from asgiref.wsgi import WsgiToAsgi
from discord_interactions import verify_key_decorator

import hypixel_api
import find_cmd
import help_cmd

DISCORD_PUBLIC_KEY = os.environ.get("DISCORD_PUBLIC_KEY")

app = Flask(__name__)
# Transform our python code to a lambda function so AWS lambda can use
asgi_app = WsgiToAsgi(app)
handler = Mangum(asgi_app)


@app.route("/", methods=["POST"])
# @verify_key_decorator(DISCORD_PUBLIC_KEY)
def interactions():
    try:
        print(f"👉 Request: {request.json}")
        raw_request = request.json
        
        if raw_request["type"] == 1:  # PING
            print("Received PING")
            return jsonify({"type": 1})  # PONG
        
        data = raw_request.get("data")
        if not data:
            raise ValueError("Data field is missing in request.")
        
        command_name = data.get("name")
        if not command_name:
            raise ValueError("Command name is missing in request data.")

        if command_name == "echo":
            original_message = data["options"][0]["value"]
            
            embed = {
                "title": "Poly the parrot",
                "description": f"Echo: {original_message}",
                "color": 0x5865F2,  # Blurple color
                "thumbnail": {
                    "url": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/d/de/Red_Parrot.png/revision/latest?cb=20170720112713"
                },
            }

            response_data = {
                "type": 4,
                "data": { "embeds": [embed] },
            }
        elif command_name == "help":
            embed = {}
            if "options" in data and data["options"]: 
                embed = help_cmd.make_help_embed(data["options"][0]["value"])
            else: 
                embed = help_cmd.make_help_embed()
            
            response_data = {
                "type": 4,
                "data": { "embeds": [embed] },
            }
        elif command_name == "find":
            map_name, mode_tpye = data["options"][0]["value"], data["options"][1]["value"]
            embeds = []
            for player_name in data["options"][2:]:
                player_data = hypixel_api.get_player_data(player_name["value"])
                embed_list = find_cmd.make_player_data_embed_base(player_data, player_name["value"], map_name, mode_tpye)
                
                for embed in embed_list: 
                    embeds.append(embed)
            
            response_data = {
                "type": 4,
                "data": {"embeds": embeds},
            }

            # response_data = {
            #     "type": 4,
            #     "data": {"content": "It Works"},
            # }
        else:
            response_data = {
                "type": 4,
                "data": {"content": "Unknown command"},
            }

        return jsonify(response_data)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"type": 4, "data": {"content": f"An error occurred: {str(e)}"}})

if __name__ == "__main__":
    app.run(debug=True)
