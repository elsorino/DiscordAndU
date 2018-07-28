
from nintendo.nex import backend, authentication, friends, nintendo_notification
from nintendo import account
import rpc
import time

client_id = '472185292636291082'
rpc_obj = rpc.DiscordIpcClient.for_platform(client_id)
print("RPC connection successful.")

# Wii U Console Details
DEVICE_ID = 1111111111
SERIAL_NUMBER = "xxxxxxxxxxxx"
SYSTEM_VERSION = 0x230 # 5.5.2E
REGION = 4 # Europe (PAL)
COUNTRY = "GB" # United Kingdom (Great Britain)

# Wii U Secondary User/Account Details
USERNAME = "PutSecondaryNNIDUsernameHere"
PASSWORD = "PutSecondaryNNIDPasswordHere"

# Wii U Main User/Account NNID
MAINID = "PutMainNNIDUsernameHere"


class NotificationHandler(nintendo_notification.NintendoNotificationHandler):
	def __init__(self):
		self.name_cache = {}

	def process_notification_event(self, event):
		pid = event.pid
		if pid not in self.name_cache:
			self.name_cache[pid] = api.get_nnid(pid)
		name = self.name_cache[pid]
		
		if event.type == nintendo_notification.NotificationType.LOGOUT:
			
			if name == MAINID:
				print("Peace!")
				activity = {
					
				}
				rpc_obj.set_activity(activity)
			
		elif event.type == nintendo_notification.NotificationType.PRESENCE_CHANGE:
			presence = event.data
			
			if name == MAINID:
				print("Gotcha!")
				
				title_id = "%016X" %(event.data.game_key.title_id)
				
				if title_id == "0000000000000000":
					title_name = "Wii U Menu"
				elif title_id == "000500001010ED00":
					title_name = "MARIO KART 8"
				elif title_id == "000500001010CD00":
					title_name = "MARIO KART 8"
				elif title_id == "0005000010176A00":
					title_name = "Splatoon"
				elif title_id == "00050000101C9500":
					title_name = "Breath of the Wild"
				elif title_id == "0005000010180700":
					title_name = "Captain Toad: Treasure Tracker"
				elif title_id == "0005000010199500":
					title_name = "Super Mario 64"
				elif title_id == "0005000010195B00":
					title_name = "NEW SUPER MARIO BROS."
				elif title_id == "0005000010172700":
					title_name = "BAYONETTA 2"
				elif title_id == "000500301001420A":
					title_name = "Nintendo eShop"
				elif title_id == "000500301001620A":
					title_name = "Miiverse"
				elif title_id == "000500301001220A":
					title_name = "Internet Browser"
				elif title_id == "000500101004A200":
					title_name = "Mii Maker"
				elif title_id == "000500101005A200":
					title_name = "Wii U Chat"
				elif title_id == "0005000010105A00":
					title_name = "Netflix"
				elif title_id == "0005000010105700":
					title_name = "YouTube"
				elif title_id == "0005000010102F00":
					title_name = "Amazon / LOVEFiLM"
				elif title_id == "0005000010101E00":
					title_name = "New SUPER MARIO BROS. U"
				elif title_id == "000500001014B800":
					title_name = "New SUPER MARIO BROS. U + New SUPER LUIGI U"
				elif title_id == "0005000010145D00":
					title_name = "SUPER MARIO 3D WORLD"
				elif title_id == "000500001018DD00":
					title_name = "Super Mario Maker"
				else:
					title_name = title_id
					
				#idDash = title_id[:8] + "-" + title_id[8:]
				#print("idDash: " + idDash)
					
				start_time = time.time()
				print(title_id + " / " + title_name)
				
				activity = {
					"details": title_name,
					"timestamps": {
						"start": start_time
					},
					"assets": {
						"small_text": MAINID,
						"small_image": "nn",
						"large_text": title_name,
						"large_image": title_id.lower()
					}
				}
				rpc_obj.set_activity(activity)
		else:
			print("Unknown notification type %i (from %s)" %(event.type, name))

api = account.AccountAPI()
api.set_device(DEVICE_ID, SERIAL_NUMBER, SYSTEM_VERSION, REGION, COUNTRY)
api.set_title(friends.FriendsTitle.TITLE_ID_EUR, friends.FriendsTitle.LATEST_VERSION)
api.login(USERNAME, PASSWORD)

nex_token = api.get_nex_token(friends.FriendsTitle.GAME_SERVER_ID)
backend = backend.BackEndClient(
	friends.FriendsTitle.ACCESS_KEY,
	friends.FriendsTitle.NEX_VERSION,
	backend.Settings("friends.cfg")
)
backend.connect(nex_token.host, nex_token.port)
backend.login(
	nex_token.username, nex_token.password, None,
	authentication.NintendoLoginData(nex_token.token)
)
backend.nintendo_notification_server.handler = NotificationHandler()

input("Press enter to disconnect and exit\n")
backend.close()
