import os
import traceback
from flask import Flask, jsonify, request
from mangum import Mangum
from asgiref.wsgi import WsgiToAsgi
from discord_interactions import verify_key_decorator
import boto3

import cmd_interact


DISCORD_PUBLIC_KEY = os.environ.get("DISCORD_PUBLIC_KEY")

app = Flask(__name__)
# Transform our python code to a lambda function so AWS lambda can use
asgi_app = WsgiToAsgi(app)
handler = Mangum(asgi_app)

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("hypixel-api-data-cache")

@app.route("/", methods=["POST"])
@verify_key_decorator(DISCORD_PUBLIC_KEY)
def interactions():
    try:
        print(f"👉 Request: {request.json}")
        raw_request = request.json
        
        if raw_request["type"] == 1:  # PING
            print("Received PING")
            return jsonify({"type": 1})  # PONG
        
        if raw_request["type"] == 3:  # Component (Button) Interaction
            command_args = raw_request["data"]["custom_id"].split('-')
            if command_args[0] == "find":
                response_data = { "type": 7, } # Update the message
                return_data = cmd_interact.find(table, command_args[1], command_args[2:], True)
                response_data["data"] = return_data
                return jsonify(response_data)
        
        
        data = raw_request.get("data")
        if not data: raise ValueError("Data field is missing in request.")
        command_name = data.get("name")
        if not command_name: raise ValueError("Command name is missing in request data.")

        response_data = { "type": 4, }
        if command_name == "echo":
            return_data = cmd_interact.echo(data)
            response_data["data"] = return_data
        elif command_name == "help":
            return_data = cmd_interact.help(data)
            response_data["data"] = return_data
        elif command_name == "find":
            return_data = cmd_interact.find(table, data["options"][0]["value"], [], False)
            response_data["data"] = return_data
        else: response_data["data"] = {"content": "Unknown command"}

        return jsonify(response_data)
    except Exception as e:
        traceback_str = traceback.format_exc()
        print(f"Error: {e}")
        print(traceback_str)
        return jsonify({"type": 4, "data": {"content": f"An error occurred: {str(e)}"}})

if __name__ == "__main__":
    app.run(debug=True)
