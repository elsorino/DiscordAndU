
from nintendo.nex import backend, authentication, notification
from nintendo.games import Friends
from nintendo import nnas
from pypresence import Presence
import time
from config import (
	DEVICE_ID,
	SERIAL_NUMBER,
	SYSTEM_VERSION,
	REGION,
	COUNTRY,
	LANGUAGE,
	USERNAME,
	PASSWORD,
	MAINID,
	client_id
)
RPC = Presence(client_id,pipe=0)
RPC.connect()
print("RPC connection successful.")

class NotificationServer(notification.NintendoNotificationServer):
	def __init__(self):
		super().__init__()
		self.name_cache = {}
		
	def process_nintendo_notification_event(self, context, event):
		pid = event.pid
		if pid not in self.name_cache:
			self.name_cache[pid] = nnas.get_nnid(pid)
		name = self.name_cache[pid]
		
		if event.type == notification.NintendoNotificationType.LOGOUT:
			if name == MAINID:
				print("Clearing status")
				RPC.clear()
			
		elif event.type == notification.NintendoNotificationType.PRESENCE_CHANGE:
			if name == MAINID:
				title_id = "%016X" %(event.data.game_key.title_id)
				if title_id == "0000000000000000":
					title_name = "Wii U Menu"
				elif title_id == "000500001010EC00":
					title_name = "Mario Kart 8"
				elif title_id == "000500001010CD00":
					title_name = "Splatoon"
				elif title_id == "00050000101C9400":
					title_name = "Breath of the Wild"
				elif title_id == "0005000010180700":
					title_name = "Captain Toad: Treasure Tracker"
				elif title_id == "0005000010199500":
					title_name = "Super Mario 64"
				elif title_id == "0005000010195B00":
					title_name = "New Super Mario Bros."
				elif title_id == "0005000010172700":
					title_name = "Bayonetta 2"
				elif title_id == "000500301001420A":
					title_name = "Nintendo eShop"
				elif title_id == "000500301001620A":
					title_name = "Miiverse"
				elif title_id == "000500301001210A":
					title_name = "Internet Browser"
				elif title_id == "000500101004A200":
					title_name = "Mii Maker"
				elif title_id == "000500101005A200":
					title_name = "Twilight Princess HD"
				elif title_id == "0005000010143500":
					title_name = "Wind Waker HD"
				elif title_id == "0005000010102F00":
					title_name = "New Super Mario Bros. U"
				elif title_id == "000500001014B800":
					title_name = "New Super Mario Bros. U + New Super Luigi U"
				elif title_id == "0005000010145D00":
					title_name = "SUPER MARIO 3D WORLD"
				elif title_id == "000500001018DD00":
					title_name = "Super Mario Maker"
				elif title_id == "0005000013374842":
					title_name = "Homebrew Launcher"
				elif title_id == "000500001019d800":
					title_name = "Xenoblade Chronicles"
				elif title_id == "00050000101C4D00":
				    title_name = "Xenoblade Chronicles X"
				#Example of what another entry should look like
     			#elif title_id == "TITLE_ID":
				#	title_name = "Game Name"
				else:
					title_name = title_id
				start_time = int(time.time())
    
				print(title_id + " / " + title_name)
				RPC.update(state=title_name, start=start_time, small_image="nn", small_text=MAINID, large_image=title_id.lower())
				
		else:
			print("Unknown notification type %i (from %s)" %(event.type, name))
		
	def process_presence_change_event(self, context, event):
		self.process_nintendo_notification_event(context, event)


nnas = nnas.NNASClient()
nnas.set_device(DEVICE_ID, SERIAL_NUMBER, SYSTEM_VERSION)
nnas.set_locale(REGION, COUNTRY, LANGUAGE)
nnas.set_title(Friends.TITLE_ID_EUR, Friends.LATEST_VERSION)
nnas.login(USERNAME, PASSWORD)

nex_token = nnas.get_nex_token(Friends.GAME_SERVER_ID)
backend = backend.BackEndClient("friends.cfg")
backend.configure(Friends.ACCESS_KEY, Friends.NEX_VERSION)
backend.connect(nex_token.host, nex_token.port)

login_data = authentication.NintendoLoginData()
login_data.token = nex_token.token
backend.login(
	nex_token.username, nex_token.password, None,
	login_data
)
backend.secure_client.register_server(NotificationServer())

input("Press enter to disconnect and exit\n")
backend.close()
