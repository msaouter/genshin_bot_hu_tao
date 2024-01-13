<h1 align="center">
  <br>
  <a href="https://github.com/msaouter/genshin_bot_hu_tao"><img src="https://i.postimg.cc/0Q3nZY11/202192171841.png" alt="Red - Discord Bot"></a>
  <br>
  Hu Tao
  <br>
</h1>

<h4 align="center">Hoyolab connection and free Epic Games store reminder, birthday reminder and role assigner</h4>
<p align="center">Python 3.10 - Discord.py </p>

<p align="center">
  <a href="#overview">Overview</a>
  •
  <a href="#installation">Installation</a>
  •
  <a href="https://github.com/msaouter/genshin_bot_hu_tao/wiki">Documentation</a>
  •
  <a href="#disclaimer">Disclaimer</a>
  •
  <a href="#license">License</a>
</p>


# Overview
<p>HuTao is small bot created by a video game programer and genshin impact enthusiast to help her discord server. At the moment the 1.1 version is released, HuTao can't be added to your server because of the lack of tutorial to include it correctly and missing functionnalities and hard coded functionalities. 

HuTao is a discord bot that have multiple functionnalities :
• Role assigner - Need something that can assign mulitple roles for your server ? I've got you covered ! Hu Tao can post a message on a designated channel to list the available roles and assign a role to a user who react to the message with the chosen emoji (customized or not).

• Genshin Impact daily connection reminder - Connect to Hoyolab everyday to get primogems, moras, weapon crystals and food for your game. The bot is able to send you a message everyday at 8pm (server local time) to remind you that you have to check-in for the daily connection. The message have a clickable link that will guide you to the connection page so that you won't have to search for the link, very useful !

• Epic Games weekly reminder - Every week, the Epic Games Store is offering a free game for a week to everyone who owns an account on their shop. To stop forgetting about claiming your game, you can add this bot to your server to get a reminder every thursday at 5pm. Like the genshin reminder, the reminder have a direct link to the Epic Games store on the posted message so that you don't have to search for the link.

• Prime gaming monthly reminder - Every month, Prime Gaming is offering in-game contents and free games to all Amazon Prime subscribers, to not miss any rewards, the HuTao bot can send you monthly reminder every 15th of the month to go fetch your rewards on the Prime gaming website.

• Birthday reminder - Don't forget about the birthdays of your members thanks to this bot ! Every day, the bot will check if today is the birthday of one or multiple members of your server and post a message if that's the case. *Available in 2.0 version*

• Music bot - Want to listen to music while your in vocal with your friends ? HuTao can do this for you. Use the music commands to play, pause, stop, forward to the next song and add a music to the playing queue. *Available in 2.0 version*</p>


# Installation
<p>HuTao is small bot created by a video game programer and genshin impact enthusiast to help her discord server. At the moment the 1.2 version is released, HuTao can be added to your server but not via the Add Application button and it may be lacking some of it's core feature like the birthdays management or the full management of the roles.

To install HuTao on your server, you'll need a server or a computer that will be powered 24/7 to act as a server or you may chose to not have it always running. You'll also need to activate the <a href="https://techswift.org/2020/09/17/how-to-enable-developer-mode-in-discord/">developper mode of discord</a> and to download a python editor like <a href="https://www.jetbrains.com/fr-fr/pycharm/download/?section=windows">pyCharm</a> which is free and my prefered IDE.

First of all, do not use the button "Add this application", the bot needs a config file with your server ID at the moment. </p>

## Server creation
To host this bot, you'll need your own server. Here's 3 possible options :
- Use your personnal computer. This means that to leave it operationnal 24/7, you'll need to let your computer run. The bot can be shutdown / restarted without any problem at the 1.2 version so even if you don't want it to be able to operate at any time, this is totally ok and the only thing you'll need to remind yourself is to launch the bot programm when you start your computer.
- Buy a Raspberry Pi and host it on it. This is the solution I'm currently using. I'm using the Zero 2 W board. This is probably the best compromise of all 3 options as the small board doesn't take a lot of place, can run 24/7 and doesn't take too much electricity.
- Use an online service of python discord bot hosting. You can find free or paid services, I don't have any recommandation as the free ones i used to use are now closed.

## Config file creation
Once you've copied this repository, you'll need to create a config file called config and to change the production variable to True. Let's do the first thing. 
Go to genshin_bot_hu_tao\Bot_discord\Bot_discord folder, inside this folder you'll the .py files. Do a right click and go to New -> Text file. Name the new file "config" without any extension. Click ok on the warning windows that may appear telling you that removing the extension may broke the file. Open it on the windows bloc note and paste this format :
```
TOKEN=
CHANNEL_ROLE=
CHANNEL_REMIND=
CHANNEL_ANSWER=
CHANNEL_BIRTHDAYS=
GUILD=
GENSHIN_ROLE=
EPIC_GAMES_ROLE=
PRIME_GAMING=
```

Here's how to complete it :
- The token is your bot token, it is striclty personnal and if found anywhere online, discord will automatically change it. Don't mess with it. To retrieve your bot token <a href="https://www.writebots.com/discord-bot-token/">here's a perfect tutorial by writebots.</a> Just a reminder : if you forget your token, you'll need to reset it.
- The channel_role/remind/answer/birthdays is the channel id where you want the bot to post messages for any of these actions. For this, you'll need <a href="https://beebom.com/how-enable-disable-developer-mode-discord/">the developer mode enabled</a> on your discord. Once it's activated, you can right click on the channel and click on Copy channel ID and paste it on the corresponding lines.
- The guild is the server id. To get it, you can either right click on the server name if you're on it or on the server icon on the left bar and click Copy server ID.
- The genshin/Epic/Prime_role is the roles ids. To get them, right click on the server name or icon -> server parameters -> roles. A right click on the role will allow you to see the Copy role ID option. Paste it onto the corresponding lines

When you paste them onto your file, do not add any space between the "=" symbol and your numbers. Save it and you're done. With the config file complete, you're almost ready and the most difficult part is done.

## Production value to True
As I said in the precedent section, there's one variable to change. This variable is here to allow you to test the bot before launching it on your server or for me to test the next features i'm programming without disturbing my main bot. To use your bot on your server with your config file, open the file HuTaoBot.py
On top of the file, you'll find a section called GLOBAL. Inside this section, you'll find a variable called production set to False. Change False to True (the caps is important otherwise you won't be able to launch the bot). Save and you're ready to finally launch it.
<img width="488" alt="the global section with the production values right after the import lines" src="https://github.com/msaouter/genshin_bot_hu_tao/assets/45098192/d4253e33-3843-4a09-a5ef-c74deb8984bc">


## Start the bot
I'll write here only how to start it locally on your computer or on a raspberry. If you chose to go with the server option, please see with your server how to start a discord bot. If you're on your personnal computer with pyCharm, open the HuTaoBot.py and click on the run option on the top far right of your screen. A console will open on the bottom of your pyCharm interface. Once you see the message "bot_name is ready !", this is functionnal. 

If you're not on pyCharm, any coding environnement will have a run option, find it, click on it and it'll normally open a console command and show you the same message when it can receive commands.
On raspberry OS, open the terminal by doing a right click on an empty space of the file manager and terminal. Once you have the process open, enter this following line :
```
python HuTaoBot.py
```
On the terminal you'll see the message "bot_name is ready !" which means the bot can answer you.

To test the bot, on your answer channel you can try the command "!hutao", she'll greet you.

## Initialize the role attribution function
HuTao is able to manage the genshin/epic/prime role when initialized. You can always attribute them yourself by hand but why waste your time when you can automate it ?
To initialize her role management function, write on your role assignement channel the command "!init". Once this command is send, HuTao will post a message to show you the emotes to react to get the corresponding reminder roles.

## End note
This process is an experimentation, i'm not fully certain the installation process is working but it's similar to any discord bot which needs you to own the application on your account. I plan in the future to have a full compatibility with the "Add application" button.


# Disclaimer
<p>HuTao is small bot created by a video game programer and genshin impact enthusiast to help her discord server. I don't promise regular updates as I made this project for fun, I can't promise to add what you want because I add in priority what my guild needs and what's in my programming capacities. This may stop receving updates at any moments by a lack of time or not wanting to add anything else.


# License
<p>Released under the <a href="https://choosealicense.com/licenses/mit/">MIT</a> license.

Hu Tao is named after the pyro character from "Genshin Impact", a video game by <a href="https://genshin.mihoyo.com/">MiHoYo</a>.

In game picture taken by Marion Saouter inside the game "Genshin Impact".

The template of this Readme file is inspired by the <a href="https://github.com/Cog-Creators/Red-DiscordBot#readme">Red-DiscordBot</a> one.

This project is created by myself, Marion Saouter.</p>
