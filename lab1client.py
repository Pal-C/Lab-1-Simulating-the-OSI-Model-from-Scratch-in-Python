# Lab 1: Simulating the OSI Model from Scratch in Python

import socket
import json

class Application_layer:    # Simulates the HTTP-like request-response communication
    def send(self, message):    # Function that simulates the sending of data (messages) as a request
        request = {"method": "GET", "message": message} 
    
        return json.dumps(request)  # stores the request in a json file format
    
    def receive(self, request):     # Function that simulates the receiving of a request (here it just parses the JSON request and extracts the data (message))
        response = json.loads(request)  # loads the message / request from the JSON file  

        return response["message"]  

class Presentation_layer:   # Simulates the encryption, compression, encoding, and vice versa of the 3 actions on parsed data
    def encrypt(self, data, key = 5):   # Function that encrypts data with a key of 5

        return "".join(chr(ord(char) ^ key) for char in data)   # Encrypts the data by converting the data to 
                                                                # ASCII then applies the XOR operation with the key
                                                                # for each char in data and combines them afterward
    
    def compress(self, data):   # Function that compresses the data using the Run-Length Encoding (had to search for this heh) process
        compressed = []
        length = len(data)
        i = 0
        while i < length:
            count = 1
            while i + 1 < length and data[i] == data[i+1]:
                count += 1
                i += 1
            compressed.append(f"{data[i]}{count}")
            i += 1

        return "".join(compressed)
    
    def encode(self, data,):    # Function that returns the data after encryption and compression... 'encoding' :D
        encrypted = self.encrypt(data)

        return self.compress(encrypted)
    
    def decrypt(self, data, key = 5):   # Function that decrypts the data (basically undo-ing encryption)
        return "".join(chr(ord(char) ^ key) for char in data)

    def decompress(self, data): # Function that decompresses run-length encoded data (basically undo-ing the compression process)
        decompressed = []
        length = len(data)

        i = 0
        while i < length:
            char = data[i]
            if i + 1 < length:
                count = int(data[i+1])
            else:
                count = 1
            decompressed.append(char * count)
            i += 2

        return "".join(decompressed)

    def decode(self, data): # Function that decodes the data by decrypting then decompressing
        decoded = self.decrypt(data)

        return self.decompress(decoded)
    
class Session_layer:    # Simulates the managing of session data (both functions just pass data actually for this simulation-)
    def send(self, data):
        return data
    
    def receive(self, data):
        return data

class Transport_layer:  # Simulates the TCP-like segmentation and sequencing of data
    def send(self, data):  
        segment = {"seg": 1, "data": data}  # Wraps data in a transport segment

        return json.dumps(segment)  # Stores the segment into JSON format
    
    def receive(self, data):
        segment = json.loads(data)  # Parses JSON data back into Python dict.

        return segment["data"]  # Extracts the data :D

class Network_layer:    # Simulates IP adressing and packet routing
    def __init__(self, ip_address): # Initializes the ip address
        self.ip_address = ip_address

    def send(self, data):   # Function that wraps the data in a packet and 'sends' the data
        packet = {"IP": self.ip_address, "data": data}

        return json.dumps(packet)
    
    def receive(self, data):    # Function that loads the packet and extracts the data
        packet = json.loads(data)

        return packet["data"]


class Datalink_layer:   # Simulates MAC addressing and frame transmission
    def __init__(self, mac_address):    # Initializes the mac address
        self.mac_address = mac_address  

    def send(self, data):   # Function that wraps data in a frame and stores it into JSON format
        frame = {"mac": self.mac_address, "data": data}

        return json.dumps(frame)
    
    def receive(self, data):    # Function that loads the fram and extracts the data
        frame = json.loads(data)

        return frame["data"]

class Physical_layer:   # Simulates bit-level transmission over a network (had a lot of help from the net with this part-)
    def __init__(self, mode, host, port = 1111):    
        self.mode = mode    # Initializes the mode (server or client)
        self.host = "local" # Defines the host address (make it host for now)
        self.port = port    # Initializes the port number
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates the TCP socket
        
        if mode == "server":
            self.sock.bind((host, port))    # Binds the socket to the specified address and port
            self.sock.listen(1) # Listens for incoming connections (limit to 1 connection)

            self.conn, _ = self.sock.accept()  # Accepts the first incoming connection
        
        elif mode == "client":  
            self.sock.connect((host, port)) # Connects tot he specified server

    def send(self, data):   # Function that converts characters into bits and transmits them
        bits = "".join(format(ord(char), '08b') for char in data)   # Converts each character into an 8-bit binary
        self.sock.sendall(bits.encode())    # Sends the binary data over the network

    def receive(self):  # Receives bits and converts them back to characters
        bits = self.conn.recv(1024).decode()    # Receives binary data from the socket
        data = "".join(chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8))    # Converts binary back to text

        return data

    def close(self):
        self.sock.close()

print("TESTING CLIENT")
# Testing Client (Sender)

# Initialize layers
app = Application_layer()
pres = Presentation_layer()
sess = Session_layer()
trans = Transport_layer()
net = Network_layer(ip_address="192.168.1.1")
datalink = Datalink_layer(mac_address="00:1A:2B:3C:4D:5E")
phys = Physical_layer(mode="client", host="localhost", port=1111)

# Message to send
message = "Hello, OSI!"

print(f"\n[Client] Sending message: {message}")

# Process through OSI layers (Top to Bottom)
data = app.send(message)
print(f"[Application Layer] Encapsulated: {data}")

data = pres.encode(data)
print(f"[Presentation Layer] Encrypted & Compressed: {data}")

data = sess.send(data)
print(f"[Session Layer] Session managed: {data}")

data = trans.send(data)
print(f"[Transport Layer] Segmented: {data}")

data = net.send(data)
print(f"[Network Layer] Packaged with IP: {data}")

data = datalink.send(data)
print(f"[Data Link Layer] Framed with MAC: {data}")

# Send through Physical Layer
phys.send(data)
print(f"[Physical Layer] Sent as bits: {data}")

# Close the connection
phys.close()
