import requests
import yaml


TOKEN = "DISCORD_BOT_TOKEN"
APPLICATION_ID = "DISCORD_BOT_APPLICATION_ID"
URL = f"https://discord.com/api/v10/applications/{APPLICATION_ID}/commands"


with open("discord_commands.yaml", "r") as file:
    yaml_content = file.read()

commands = yaml.safe_load(yaml_content)
headers = {"Authorization": f"Bot {TOKEN}", "Content-Type": "application/json"}

# Send the POST request for each command
for command in commands:
    response = requests.post(URL, json=command, headers=headers)
    command_name = command["name"]
    if response.status_code == 201 or response.status_code == 200:
        print(f"Command {command_name} created successfully: {response.status_code}")
    else:
        print(f"Failed to create guild command {command_name}: {response.status_code}")
        print(f"Response: {response.text}")
        print(f"Request payload: {command}")
        print(f"Response headers: {response.headers}")
