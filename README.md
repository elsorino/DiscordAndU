# DiscordAndU (WIP)
Show your Discord friends what Wii U game you're playing!

![Image Preview](https://i.imgur.com/jUpVsFU.png)

## How does this work?
This Python program uses code from ![NintendoClients](https://github.com/Kinnay/NintendoClients) and ![python-discord-rpc](https://github.com/suclearnub/python-discord-rpc) to log into a Wii U account (with NNID linked), and view your status on the Wii U Friend List, and from there the script should automatically detect your Discord instance running on your PC and display what game you are playing!

## Prerequisites
* Python 3
* Git
* Discord
* Wii U Console
* Wii U User/Account (Must have NNID linked)
* Secondary Wii U User/Account (Must also have DIFFERENT NNID linked)
* Wii U Console Details
	* Device ID (Can be found using either ![Fiddler](https://www.telerik.com/download/fiddler) or by following ![this](https://gbatemp.net/threads/question-how-can-i-find-my-device-id.487981/#post-7661403))
	* Serial Number (Found on bottom side at rear of console)
	* System Version (0x230 for 5.5.2)
	* System Region (4 for Europe)
	* System Country (GB for United Kingdom (Great Britain))

## Download
`git clone https://github.com/2secslater/DiscordAndU.git && cd DiscordAndU`
