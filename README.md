# Applesauce 
[![](https://img.shields.io/badge/python-3.4+-blue.svg)](https://www.python.org/download/releases/3.4.0/) 
[![discord.py](https://img.shields.io/badge/discord.py-1.3.4-blue.svg)](https://github.com/Rapptz/discord.py)
[![CodeFactor](https://www.codefactor.io/repository/github/mpsparrow/applesauce/badge)](https://www.codefactor.io/repository/github/mpsparrow/applesauce)

Applesauce is a lightweight Discord bot framework that provides a plugin (cog) management system. This framework provides all the basics for a Discord bot without being bloated and confusing.

Applesauce is made with the idea of you hosting and customizing your own instance of the bot. At the moment I have no plans for making my instance of Applesauce public for people to add to their servers.

### Warning
This repo is very much so still in beta.

## Install
Make sure Python 3.4+ is running properly and pip is installed.
1. `git clone -b master https://github.com/mpsparrow/applesauce` or [download](https://github.com/mpsparrow/applesauce/archive/master.zip) and unzip 
2. `pip install -r requirements.txt`
3. open `config.ini` and add your Discord token
4. create a MongoDB database and put the connection information into `config.ini` under `MongoDB`
5. `python run.py`

## Troubleshooting
Applesauce logs everything so that it is easy to troubleshoot what and where errors are occuring. All the main logs are kept in the `logs` folder (created on first startup).

- `discord.log` logs everything from modules, discordpy, Applesauce
- `plugins.log` main log for plugin related errors
- `runtime.log` logs framework errors
- `startup.log` logs bootup of framework tasks; initial loading of plugins, checks, etc

## Wiki
Coming soon(ish)