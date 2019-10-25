# Applesauce
## WARNING
I suck at coding. I try my best but please don't get mad if you come across some crap code 😕. Applesauce is also currently in the very early stages of development. Lots of things are missing.

### Goal
The goal of Applesauce is to provide a modular approach to how a Discord bot is created and customized for each server. Applesauce uses a central `config.ini` along with individual modules for each special command/feature. Each module is fully independent from one another and is loaded automatically through `initialize.py`. This allows Applesauce to quickly be customized to only include modules you want.

This is a personal project. I am creating this with myself and my usages in mind. That being said I am more then open to any feedback or help you may have.

### Configuration
Still being worked on....

### Modules
* **admin** (required): commands to reload and manage modules
* **api**: Wikipedia and Wolfram Alpha lookup commands
* **basic**: random number, coin flip, and other simple commands
* **debug**: debug commands
* **error** (required): logs error messages
* **help** (required): compiles help command
* **moderation**: basic ban, kick, clear commands
* **reactions**: randomly adds emoji reactions to messages
