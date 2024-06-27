# Discord Bot on AWS Lambda

This repository contains the code for a personal Discord bot hosted on AWS Lambda. The primary function of the bot is to retrieve information from the Hypixel Public API about a specified player, particularly focusing on the player's stats related to the Arcade game: Zombies. Please note that this application is in no way affiliated with or endorsed by Hypixel.

The bot utilizes the [Discord Interactions Endpoint](https://discord.com/developers/docs/interactions/application-commands) to handle interactions.

The application is built with [Flask](https://flask.palletsprojects.com/) to create an HTTP server. The server is hosted on AWS Lambda using a Docker container, managed with [AWS CDK](https://aws.amazon.com/cdk/).

To use the bot, the Discord application's interactions endpoint is set to the URL of the hosted server on your [Discord Developer Portal](https://discord.com/developers/applications).