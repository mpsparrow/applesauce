# Applesauce 
[![](https://img.shields.io/badge/python-3.4+-blue.svg)](https://www.python.org/download/releases/3.4.0/) 
[![discord.py](https://img.shields.io/badge/discord.py-1.3.3-blue.svg)](https://github.com/Rapptz/discord.py)
[![CodeFactor](https://www.codefactor.io/repository/github/mpsparrow/applesauce/badge)](https://www.codefactor.io/repository/github/mpsparrow/applesauce)

Applesauce is a lightweight Discord bot framework that provides a cog management system for [discord.py](https://github.com/Rapptz/discord.py). The framework provides all the fundamentals of a bot. Cogs can be loaded to add functionality. Applesauce is fully customizable across unlimited Discord servers.

Unlike conventional Discord bots, Applesauce is made with the idea of you hosting and customizing your own instance of the bot. At the moment I have no plans for making my instance of Applesauce public for people to add to their servers.

### Warning
This repo is very much so still in beta.

## Install
Make sure Python 3.4+ is running properly and pip is installed.
1. `git clone -b master https://github.com/mpsparrow/applesauce` or [download](https://github.com/mpsparrow/applesauce/archive/master.zip) and unzip 
2. `pip install -r requirements.txt`
3. open `mainConfig.ini` and add your Discord token
4. create a mySQL database and put the connection information into `mainConfig.ini` under `mySQL`
5. run `python startup.py`

## Branches
- `master` stable release code
- `untested` unstable pre-release code and testing
