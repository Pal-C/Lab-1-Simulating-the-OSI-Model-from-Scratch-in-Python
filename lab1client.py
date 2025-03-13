# Lab 1: Simulating the OSI Model from Scratch in Python
import uuid
import socket
from main import Application_layer, Presentation_layer, Session_layer, Transport_layer, Network_layer, Datalink_layer, Physical_layer

def get_ip():  # Function that 'gets' the IP of the client side for sending
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Creates a UDP socket

  try:
    s.connect(("8.8.8.8", 80))  # Connect to an external server
    ip = s.getsockname()[0]    # Gets the IP address assigned to this client (connection)
  except Excception:
    ip = "127.0.0.1"  # If there's an error, default to localhost
  finally:
    s.close()
  return IP

def get_mac():  # Function that 'gets' the MAC address of the client side
  return ':'.join(f"{(uuid.getnode() >> i) & 0xFF:02X}" for i in range(0, 48, 8))  # Uses uuid.getnode() to get the MAC address and 
                                                                                   # converts it to a readable format :D

print("TESTING CLIENT")
# Testing Client (Sender)

# Initialize layers
app = Application_layer()
pres = Presentation_layer()
sess = Session_layer()
trans = Transport_layer()

ipad = get_ip()
mad = get_mac()

net = Network_layer(ip_address=ipad)
datalink = Datalink_layer(mac_address=mad)
phys = Physical_layer(mode="client", host="", port=1111)

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
