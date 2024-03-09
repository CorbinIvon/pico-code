# Hardware Used
- [Raspberry Pi Pico WH (Pre-Soldered Headers)](https://www.pishop.us/product/raspberry-pi-pico-wh-pre-soldered-headers/?src=raspberrypi)
- USB-A to Micro-USB-B cable, 45cm, Black (USB 2.0)
- My home WiFi network
# Files
- connect_to_SSID.py - A basic example that connects to a WiFi network and outputs the device's IP.
- get_data_from_ip.py - A bare bones example that reads the content from a web page. If the site contains plain text, it will output the plain text.
# Other Information
Read more on WLAN methods [here](https://docs.micropython.org/en/latest/library/network.WLAN.html)
# Walkthroughs
## connect_to_SSID.py
You must replace the following variables:
1. SSID = 'YOUR WIFI NAME'
2. PASSWORD = 'YOUR WIFI PASSWORD'
When running your code, you should see the following output, or something similar:
`On Success`
```bash
>>> %Run -c $EDITOR_CONTENT

MPY: soft reboot
Connecting to network...
Device IP: 10.1.1.17
>>>
```
`On Failure`
```bash
>>> %Run -c $EDITOR_CONTENT

MPY: soft reboot
Connecting to network...
Connection failed
>>>
```
## get_data_from_ip.py
You must replace the following variables:
1. SSID = 'YOUR WIFI NAME'
2. PASSWORD = 'YOUR WIFI PASSWORD'
3. IP = 'YOUR IP ADDRESS'
4. PORT = 'YOUR PORT'
5. PATH = 'YOUR PATH'
When running your code, you should see the following output, or something similar:
`On Success`
```bash
>>> %Run -c $EDITOR_CONTENT

MPY: soft reboot
Network config: 10.1.1.17
HTTP/1.0 302 Found
Set-Cookie: csrf-token=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX25d271cb; Path=/
Cache-Control: no-cache
Content-Type: text/html
Location: /login.html
Content-Length: 0
Connection: close
Date: Thu, 01 Jan 1970 18:40:18 GMT


>>>

```
`On Failure`
```bash
>>> %Run -c $EDITOR_CONTENT

MPY: soft reboot
Network config: 10.1.1.17
Cannot reach host: OSError
>>>
```
