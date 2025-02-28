# Lab 1: Simulating the OSI Model from Scratch in Python

from main import Application_layer, Presentation_layer, Session_layer, Transport_layer, Network_layer, Datalink_layer, Physical_layer

# Tester :D
print("TESTING SERVER")
# Testing Server (Receiver)

# Initialize layers
app = Application_layer()
pres = Presentation_layer()
sess = Session_layer()
trans = Transport_layer()
net = Network_layer(ip_address="192.168.1.1")
datalink = Datalink_layer(mac_address="00:1A:2B:3C:4D:5E")
phys = Physical_layer(mode="server", host="localhost", port=1111)

print("\n[Server] Ready to receive data...")

# Receive data from Physical Layer
data = phys.receive()
print(f"\n[Physical Layer] Received bits: {data}")

# Process through OSI layers (Bottom to Top)
data = datalink.receive(data)
print(f"[Data Link Layer] Frame extracted: {data}")

data = net.receive(data)
print(f"[Network Layer] Packet extracted: {data}")

data = trans.receive(data)
print(f"[Transport Layer] Segment extracted: {data}")

data = sess.receive(data)
print(f"[Session Layer] Session data: {data}")

data = pres.decode(data)
print(f"[Presentation Layer] Decrypted and decompressed: {data}")

data = app.receive(data)
print(f"[Application Layer] Final message: {data}")

# Close the connection
phys.close()
