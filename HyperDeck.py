import json
import socket
from time import sleep

class HyperDeck:
	def __init__(self, ip, port):
		self.ip = ip
		self.port = port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.settimeout(0.5)

	# Connect to the HyperDeck
	def connect(self):
		self.sock.connect((self.ip, self.port))
		return self._run_command('')

	def disconnect(self):
		self.sock.close()

	# Get useful live snapshot of what HyperDeck is doing
	def get_transport_info(self):
		return self._run_command('transport info')

	# Stop playback / recording
	def stop(self):
		return self._run_command('stop')


	# Play the current clip or playrannge, with an optional true/false loop
	def play(self, loop=False):
		if loop == None:
			loop = False
		if loop:
			return self._run_command('play: loop: true')
		else:
			return self._run_command('play: loop: true')


	# Choose the disk (usually 1 or 2)
	def select_slot(self, slot_id):
		return self._run_command('slot select: slot id: {}'.format(slot_id))


	# Make the clip with the provided index number the current clip
	def select_clip_with_index(self, clip_index):
		clip_index = 1 + max(clip_index, 0)
		return self._run_command('goto: clip id: {}'.format(clip_index))

	# Set a play-range from timecode to timecode in format '00:00:00:00'  ('HH:MM:SS:FF')
	def set_playrange(self, from_timecode, to_timecode):
		return self._run_command('playrange set: in: {} out: {}'.format(from_timecode, to_timecode))


	# Get a list of clips and format them into a list
	def get_clips_list(self):
		formatted_clip_list = []
		clip_list = self._run_command('clips get')
		for clip_index in range(1, int(clip_list['clip count']) + 1):
			this_clip = clip_list[str(clip_index)]
			timecodes_section  = this_clip[-23:]
			timecodes = timecodes_section.split(' ')
			formatted_clip = {}
			formatted_clip['index'] = clip_index
			formatted_clip['name'] = this_clip[:-24]
			formatted_clip['timecode'] = timecodes[0]
			formatted_clip['duration'] = timecodes[1]
			formatted_clip_list.append(formatted_clip)
		return formatted_clip_list

	# Internal run command which controls sending a command to HyperDeck
	# and getting a response
	def _run_command(self, command):
		obj_response = {}
		try:
			if len(command) > 0:
				if self._send(command):
					obj_response = self._objectify_response(self._receive())
			else:
				obj_response = self._objectify_response(self._receive())

		except:
			obj_response = {}
			obj_response['error'] = True
			obj_response['response_code'] = 999 # 'bad' error!!

		return obj_response

	# Sends a command to HyperDeck
	def _send(self, msg):
		msg += "\r\n"
		try:
			#return self.sock.send(bytes(msg, 'utf-8'))
			self.sock.sendall(msg.encode('utf-8'))
			return True
		except Exception as e:
			print("Error during send to HyperDeck:", e)
			return False

	# Receives text information back from HyperDeck
	def _receive(self):
		chunks = []
		bytes_recd = 0
		received_text = ''
		end_of_input_flag = False

		while not end_of_input_flag:
			try:
				chunk = self.sock.recv(1000)
				if chunk == b'':
					raise RuntimeError("socket connection broken")
				elif chunk == None or len(chunk) == 0:
					end_of_input_flag = True
				else:
					chunks.append(chunk)
					bytes_recd = bytes_recd + len(chunk)
					received_bytes = b''.join(chunks)
					received_text += str(received_bytes)
			except Exception as e:
				end_of_input_flag = True

		return received_text

	# Convert the text response from HyperDeck into a more disciplined object
	def _objectify_response(self, hyperdeck_response):
		data = {}
		lines = hyperdeck_response.split('\\r\\n')
		for line in lines:
			if line.startswith("b'"):
				header_items = line.split(" ")
				header_text = ""
				for item in header_items:
					if item == header_items[0]:
						data["response_code"] = int(header_items[0][2:])
					else:
						header_text += item + " "

				data['response_subject'] = header_text.strip()[:-1]

			else:
				name_value_pair = line.split(': ')
				if len(name_value_pair)  == 2:
					data[name_value_pair[0]] = name_value_pair[1]

		return data