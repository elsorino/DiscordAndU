
from nintendo.nex import service, kerberos, streams, common
import random

import logging
logger = logging.getLogger(__name__)


class ConnectionData(common.Structure):
	def streamout(self, stream):
		self.station = stream.stationurl()
		self.connection_id = stream.u32()


class SecureClient(service.ServiceClient):
	
	METHOD_REGISTER = 1
	METHOD_REQUEST_CONNECTION_DATA = 2
	METHOD_REQUEST_URLS = 3
	METHOD_REGISTER_EX = 4
	METHOD_TEST_CONNECTIVITY = 5
	METHOD_UPDATE_URLS = 6
	METHOD_REPLACE_URL = 7
	METHOD_SEND_REPORT = 8
	
	PROTOCOL_ID = 0xB
	
	def __init__(self, back_end, access_key, ticket, auth_client):
		super().__init__(back_end, access_key)
		self.ticket = ticket
		self.auth_client = auth_client
		self.kerberos_encryption = kerberos.KerberosEncryption(self.ticket.key)
		
		station_url = self.auth_client.secure_station
		self.connection_id = station_url["CID"]
		self.principal_id = station_url["PID"]
		
	def connect(self, host, port):
		stream = streams.StreamOut(self.back_end.version)
		stream.buffer(self.ticket.data)
		
		check_value = random.randint(0, 0xFFFFFFFF)
		substream = streams.StreamOut(self.back_end.version)
		substream.u32(self.auth_client.pid)
		substream.u32(self.connection_id)
		substream.u32(check_value) #Used to check connection response
		
		stream.buffer(self.kerberos_encryption.encrypt(substream.data))
		super().connect(host, port, stream.data)
		
		stream = streams.StreamIn(self.client.connect_response, self.back_end.version)
		if stream.u32() != 4: raise ConnectionError("Invalid connection response size")
		if stream.u32() != (check_value + 1) & 0xFFFFFFFF:
			raise ConnectionError("Connection response check failed")
		self.client.set_secure_key(self.ticket.key)

	def register_urls(self, login_data=None):
		local_station = common.StationUrl(
			address=self.client.get_address(), port=self.client.get_port(), sid=15, natm=0, natf=0, upnp=0, pmp=0
		)
		
		if login_data:
			connection_id, public_station = self.register_ex([local_station], login_data)
		else:
			connection_id, public_station = self.register([local_station])

		local_station["RVCID"] = connection_id
		public_station["RVCID"] = connection_id
		return local_station, public_station
		
	def register(self, urls):
		logger.info("Secure.register(%s)", urls)
		#--- request ---
		stream, call_id = self.init_request(self.PROTOCOL_ID, self.METHOD_REGISTER)
		stream.list(urls, stream.stationurl)
		self.send_message(stream)
		
		#--- response ---
		return self.handle_register_result(call_id)
	
	def register_ex(self, urls, login_data):
		logger.info("Secure.register_ex(...)")
		#--- request ---
		stream, call_id = self.init_request(self.PROTOCOL_ID, self.METHOD_REGISTER_EX)
		stream.list(urls, stream.stationurl)
		stream.add(common.DataHolder(login_data))
		self.send_message(stream)
		
		#--- response ---
		return self.handle_register_result(call_id)
		
	def handle_register_result(self, call_id):
		stream = self.get_response(call_id)
		result = stream.u32()
		connection_id = stream.u32()
		public_station = stream.stationurl()
		logger.info("Secure.register(_ex) -> (%08X, %s)", connection_id, public_station)
		return connection_id, public_station
		
	def request_connection_data(self, cid, pid):
		logger.info("Secure.request_connection_data(%i, %i)", cid, pid)
		#--- request ---
		stream, call_id = self.init_request(self.PROTOCOL_ID, self.METHOD_REQUEST_CONNECTION_DATA)
		stream.u32(cid)
		stream.u32(pid)
		self.send_message(stream)
		
		#--- response ---
		stream = self.get_response(call_id)
		result = stream.bool()
		connection_data = stream.list(lambda: stream.extract(ConnectionData))
		logger.info("Secure.request_connection_data -> (%i, %s)", result, [dat.station for dat in connection_data])
		return result, connection_data
		
	def request_urls(self, cid, pid):
		logger.info("Secure.request_urls(%i, %i)", cid, pid)
		#--- request ---
		stream, call_id = self.init_request(self.PROTOCOL_ID, self.METHOD_REQUEST_URLS)
		stream.u32(cid)
		stream.u32(pid)
		self.send_message(stream)
		
		#--- response ---
		stream = self.get_response(call_id)
		result = stream.bool()
		urls = stream.list(stream.stationurl)
		logger.info("Secure.request_urls -> (%i, %s)", result, urls)
		return result, urls
	
	def test_connectivity(self):
		logger.info("Secure.test_connectivity()")
		#--- request ---
		stream, call_id = self.init_request(self.PROTOCOL_ID, self.METHOD_TEST_CONNECTIVITY)
		self.send_message(stream)
		
		#--- response ---
		self.get_response(call_id)
		logger.info("Secure.test_connectivity -> done")
		
	def replace_url(self, url, new):
		logger.info("Secure.replace_url(%s, %s)", url, new)
		#--- request ---
		stream, call_id = self.init_request(self.PROTOCOL_ID, self.METHOD_REPLACE_URL)
		stream.stationurl(url)
		stream.stationurl(new)
		self.send_message(stream)
		
		#--- response ---
		self.get_response(call_id)
		logger.info("Secure.replace_url -> done")
		
	def send_report(self, report_id, data):
		logger.info("Secure.send_report(%i, ...)", report_id)
		#--- request ---
		stream, call_id = self.init_request(self.PROTOCOL_ID, self.METHOD_SEND_REPORT)
		stream.u32(report_id)
		stream.qbuffer(data)
		self.send_message(stream)
		
		#--- response ---
		self.get_response(call_id)
		logger.info("Secure.send_report -> done")
