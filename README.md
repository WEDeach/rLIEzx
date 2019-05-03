# rLIEzx
[![LICENSE](https://img.shields.io/badge/license-BSD%203%20Clause-blue.svg "LICENSE")](https://github.com/fadhiilrachman/line-py/blob/master/LICENSE) [![Supported python versions: 3.x](https://img.shields.io/badge/python-3.x-green.svg "Supported python versions: 3.x")](https://www.python.org/downloads/) [![Chat on Discord](https://discordapp.com/api/guilds/466066749440393216/widget.png "Chat on Discord")](https://discord.gg/9dfectq)

*牧羊人之心(繁中服) Login API*
**僅供學術研究用, 使用此API將可能被鎖號!!**

----

## Requirement

The linepy module only requires Python 3. You can download from [here](https://www.python.org/downloads/). 

## How to use
1. Install and start mitmproxy
2. Start Android emulator by using command: ```emulator -avd "YOUR_AVD_NAME" -http-proxy 127.0.0.1:8080```(You can also use your phone and set up a wifi proxy)
3. Open browser and navigate to http://mitm.it/ to trust the certificate on your emulator.
4. Login to SINoALICE(TW ver.) and until you see the main lobby
5. Go to http://127.0.0.1/8081 and filter the sniffered traffic by ```/loginUser```
6. You can find `LOGIN ENCRYPT DATA` on the "Requests" tab (make the view mode to RAW and copy it)
8. Replace it with the example string in 'getUserData.py'
9. Run!
