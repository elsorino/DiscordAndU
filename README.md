# DiscordAndU
Show your Discord friends what Wii U game you're playing!

![Image Preview](https://i.imgur.com/Md2fuZb.png)

## How does this work?
This Python program uses code from [NintendoClients](https://github.com/Kinnay/NintendoClients) and [Pypresence](https://pypi.org/project/pypresence/) to log into a Wii U account (with NNID linked), and view your status on the Wii U Friend List, and from there the script should automatically detect the Discord instance running on your PC and display what game you are playing!

## Prerequisites
### Software
* [Python 3.7](https://www.python.org/downloads/)
	* I recommend using something like pyenv for this
	* [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)
	* [Requests](https://pypi.org/project/requests/)
	* [lxml](https://pypi.org/project/lxml/)
	* [Pypresence](https://pypi.org/project/pypresence/)
* [Git](https://git-scm.com/downloads)
* [Discord](https://www.discordapp.com/)
### Wii U
* Main Wii U User/Account (Must have NNID linked)
* Secondary Wii U User/Account (Must also have DIFFERENT NNID linked)
* Wii U Console Details
	* Device ID (Best found by using [Pretendo Installer](https://github.com/PretendoNetwork/network-installer))
	* Serial Number (Found on bottom side at rear of console or in Pretendo Installer)
	* System Version (0x240 for 5.5.3, 0x250 for 5.5.4)
	* System Region (4 for Europe, 2 for USA)
	* System Country (GB for UK, US for USA)

## Download
In a terminal window, enter the following:
```bash
git clone https://github.com/elsorino/DiscordAndU.git && cd DiscordAndU
```

## Configuration 

Copy `config.example.py` to `config.py`, then open it with your preferred text editor (I recommend Vim or Notepad++), and replace the following variables with your Wii U Console details that you (hopefully) took note of earlier.

```py
DEVICE_ID = 1111111111
SERIAL_NUMBER = "xxxxxxxxxxxx"
SYSTEM_VERSION = 0x240 # 5.5.3
REGION = 4 # Europe (PAL)
COUNTRY = "GB" # United Kingdom (Great Britain)
```

Next, you'll need a secondary Wii U account with an NNID linked. Make sure to friend this account from your main account (or vice versa, just make sure that they are friends.) Also, you'll need to open Friend List on your main account, and make sure that "Allow friends to see what you are playing?" is set to Allow.

Now, underneath the Wii U Console Details in the `dau.py` file, you'll see 2 variables:
```py
USERNAME = "PutSecondaryNNIDUsernameHere"
PASSWORD = "PutSecondaryNNIDPasswordHere"
```

Finally, you'll need to change the following variable to the NNID of your main account:
```py
MAINID = "PutMainNNIDUsernameHere"
```

## Running
Make sure Discord is currently open, then open a terminal in the same directory as `dau.py` and type the following:
```bash
python dau.py
```
If you see the following output, then you should be set!
![Execution](https://i.imgur.com/um9eiKv.png)
You can now open your Wii U game of choice and show off!

## Adding/editing custom entries

If a game you play only shows the title ID without an icon, it means that the game isn't supported by default

To add a custom name for a title ID, add it to dau.py near the other entries with the following format:

```         python
#elif title_id == "TITLE_ID":
#	title_name = "Game Name"
```

You can also change existing entries the same way.

### Images

Images you wish to use for a game must be named titleid.jpg/png and be sized 512x512 or higher

If you wish to use official images, the tool [idbe-decryptp](https://github.com/NexoDevelopment/idbe_decrypt) is what I used

In order to add images, you must create a discord app on the [discord developers page](https://discord.gg/developers), Name the app what you want the status to show up as below your name(e.g the default one is named Wii U) then create.

After doing this, go to Rich Presence then art assets and add the image you created/downloaded earlier. Images should now show up if everything is named correctly. The image used for the nnid icon must be named nn.jpg/png

