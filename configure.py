import configparser

print("""
                               __                                                             
                              /  |                                                            
  ______    ______    ______  $$ |  ______    _______   ______   __    __   _______   ______  
 /      \  /      \  /      \ $$ | /      \  /       | /      \ /  |  /  | /       | /      \ 
 $$$$$$  |/$$$$$$  |/$$$$$$  |$$ |/$$$$$$  |/$$$$$$$/  $$$$$$  |$$ |  $$ |/$$$$$$$/ /$$$$$$  |
 /    $$ |$$ |  $$ |$$ |  $$ |$$ |$$    $$ |$$      \  /    $$ |$$ |  $$ |$$ |      $$    $$ |
/$$$$$$$ |$$ |__$$ |$$ |__$$ |$$ |$$$$$$$$/  $$$$$$  |/$$$$$$$ |$$ \__$$ |$$ \_____ $$$$$$$$/ 
$$    $$ |$$    $$/ $$    $$/ $$ |$$       |/     $$/ $$    $$ |$$    $$/ $$       |$$       |
 $$$$$$$/ $$$$$$$/  $$$$$$$/  $$/  $$$$$$$/ $$$$$$$/   $$$$$$$/  $$$$$$/   $$$$$$$/  $$$$$$$/ 
          $$ |      $$ |                                                                      
          $$ |      $$ |                                                                      
          $$/       $$/                                                                       
""")
print("Welcome to the applesauce configuration! This script guides you through the process of setting up your own applesauce instance.\n")
print("--- The basics ---")
token = input("Your discord token: ")
prefix = input("Command prefix [Enter to use the default (!)]: ")
if prefix == "":
    prefix = "!"
pl_folder = input("Plugin folder [Enter to use the default (plugin)]: ")
if pl_folder == "":
    pl_folder = "plugins"

print("\n--- Databse setup ---")
host = input("Hostname: ")
database = input("Database name: ")
user = input("Username: ")
password = input("Password: ")

config = configparser.ConfigParser()
config["main"] = {'discordToken': token,
                  'defaultPrefix': prefix,
                  'pluginFolder': pl_folder}

config["MongoDB"] = {'host': host,
                     'database': database,
                     'user': user,
                     'password': password}

with open("config.ini", "w+") as file:
    config.write(file)