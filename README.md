# NottABot Rewrite

NottABot Rewrite is a discord bot made expressly with the purpose of improving my skills on a proper project
There are multiple functions to this bot, but most of them pertain to Hypixel Skyblock.
Read the RUN instructions at the bottom of this README to run this for yourself.


### Learning DiscordPy By Making This Bot.

#### Discord: NottCurious#4351

## Features
* Generic Functions
    * Ping
    * Bot Version
    * Help
    * Prefix
    

* Moderation
    * Clear Messages
    * Kick User
    * Ban User
    * Unban User
    


* Hypixel
    * Player Data


* Hypixel Skyblock
    * Skill Levels 
    * Fairy Soul Data
    * Dungeon Data
      * Individual Floor Data
    * Missing Talismans
    * Pets
    * Missing Pets
    * Slayer Data
        * Zombie
        * Spider
        * Wolf
  

* Hypixel Calculators
  * Wood Prices
  * Splash Pot Prices
    * Not Really Needed Anymore, but I've always wanted to do this
    * 12, 18 and 29 pot splashes
  

* Reactions
  * A Little Like OwO Bot's Reaction Feature
    * Hug
    * Kiss
    * Pat
    * Smug
    * Cry
    * Happy
    * Shrug
    * Sleepy
    * Triggered
  

* Quick Maths
  * Factorial
  * Pow
  * Square Root
  

## To Do
* Music
  * Play
  * Queue
  * Disconnect
  * Pause
  * Shuffle Queue


* Color Reaction Roles



## Changelog
View the Changelog [here](https://github.com/nottcurious/nottabot-rewrite/blob/main/CHANGELOG.md)

### How To Run This On Your Own
#### Prerequisites
* Clone the Repository with 
```git clone https://github.com/NottABot-Rewrite.git```

* Python 3.8+
* ```pip install -r requirements.txt```
  
#### Required Files
Next, make a ```.env``` file with the following fields

```
BOTTOKEN=<insert bot token>
APIKEY=<insert hypixel api key>
BOTVERSION=Beta-v0.4
#debug info critical error warning
LOGLEVEL=<one of the above>
DISCORD_LOG_LEVEL=<one of the above>
```
Please note:
* 'Error' - Almost no Output to Screen Except Errors - Fastest 
* Critical - Very Little Output to Screen - Very Fast
* Warning - Very Little Output to Screen - Very Fast
* Info - Normal Output - Fast
* Debug - Lots of Output - Slowest

***IT IS RECOMMENDED TO USE INFO***

without ```APIKEY``` functions related to Hypixel will not work

then simply
```shell
python main.py
```

#### The Bot has To Be Online When You Make it Join a Server!!

## License
Licensed Under GNU General Public License

### APIs Used
* Mojang API to Get UUIDs
* Hypixel API for Player Data
* SkyShiiyuMoe API for Skyblock Data
* Senither Hypixel API for Skyblock Data
