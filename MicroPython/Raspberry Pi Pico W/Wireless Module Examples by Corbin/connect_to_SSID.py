import network
import time

# Configure your SSID and password here
SSID = 'YOUR WIFI NAME'
PASSWORD = 'YOUR WIFI PASSWORD'

# Initialize Wi-Fi in station mode
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

if wlan.isconnected():
    wlan.disconnect()

# Connect to the specified network
if not wlan.isconnected():
    print('Connecting to network...')
    wlan.connect(SSID, PASSWORD)

    # Wait for connection with a timeout
    timeout = 10
    while not wlan.isconnected() and timeout > 0:
        time.sleep(1)
        timeout -= 1

# Check if connected or not
if wlan.isconnected():
    print('Device IP:', wlan.ifconfig()[0])
else:
    print('Connection failed')