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

## Configuration
Open `dau.py` with your preferred text editor (I recommend Vim or Notepad++), and replace the following variables with your Wii U Console details that you (hopefully) took note of earlier.

```
DEVICE_ID = 1111111111
SERIAL_NUMBER = "xxxxxxxxxxxx"
SYSTEM_VERSION = 0x230 # 5.5.2E
REGION = 4 # Europe (PAL)
COUNTRY = "GB" # United Kingdom (Great Britain)
```

Next, you'll need a secondary Wii U account with an NNID linked. Make sure to friend this account from your main account (or vice versa, just make sure that they are friends. Also, you'll need to open Friend List on your main account, and make sure that "Allow friends to see what you are playing?" is set to Allow.

Now, underneath the Wii U Console Details in the `dau.py` file, you'll see 2 variables:
```
USERNAME = "PutSecondaryNNIDUsernameHere"
PASSWORD = "PutSecondaryNNIDPasswordHere"
```

Finally, you'll need to change the following variable to the NNID of your main account:
```
MAINID = "PutMainNNIDUsernameHere"
```

## Running
Open a terminal in the same directory as `dau.py` and type the following:
```
python3 dau.py
```
If you see the following output, then you should be set!
![Execution](https://i.imgur.com/um9eiKv.png)
You can now open your Wii U game of choice and show off!
