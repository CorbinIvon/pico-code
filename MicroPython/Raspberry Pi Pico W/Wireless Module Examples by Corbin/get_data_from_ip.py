import network
import time
import usocket

# Configure your SSID and password here
SSID = 'YOUR WIFI NAME'
PASSWORD = 'YOUR WIFI PASSWORD'

# Initialize Wi-Fi in station mode
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

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
    print('Network config:', wlan.ifconfig()[0])
else:
    print('Connection failed')


def fetch_content(ip, port, path):
    try:
        addr_info = usocket.getaddrinfo(ip, port, 0, usocket.SOCK_STREAM)[0]
        s = usocket.socket(addr_info[0], addr_info[1], addr_info[2])
        try:
            s.connect(addr_info[-1])
            request = f"GET {path} HTTP/1.0\r\nHost: {ip}\r\n\r\n"
            s.send(bytes(request, 'utf8'))
            
            response = ''
            while True:
                data = s.recv(100)
                if data:
                    response += str(data, 'utf8')
                else:
                    break
            return response
        except OSError as e:
            return "Cannot reach host: OSError"
        finally:
            s.close()
    except usocket.gaierror:
        return "Cannot reach host: usocket.gaierror"


ip = '192.168.1.1'
port = 80
path = '/' # You can adjust this path depending on the URL you're trying to access.

content = fetch_content(ip, port, path)
print(content)