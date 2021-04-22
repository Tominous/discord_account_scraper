import requests
import time
from colorama import Fore, init, Style
import string
import random
import platform
import os
import shutil
init()
operative = platform.system()
colors = {
   'green': Fore.GREEN,
   'red': Fore.RED,
   'end':Fore.RESET,
   'yellow': Fore.YELLOW,
   'bold': Style.BRIGHT
}
def clear():
   if operative == "Linux":
      os.system("clear")
   elif operative == "Windows":
      os.system("cls")
def success(text):
   print(f"[{colors['green']}!{colors['end']}] {text}")
def waiting(text):
   print(f"[{colors['yellow']}!{colors['end']}] {text}")
def error(text):
   print(f"[{colors['red']}!{colors['end']}] {text}")
def randsymbolstring(length):
   letters = string.punctuation
   return ''.join(random.choice(letters) for i in range(length))
def randstring(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))
def save(location, text=None, b=None):
   if text:
      with open(location, "a", encoding='utf-8') as f:
         f.write("\n"+text)
         f.close()
   elif not text and not b:
      os.mkdir(location)
   elif b:
      with open(location, "wb") as f:
         f.write(b)
         f.close()
def getImageFormat(url):
   if '.png' in url:
      return '.png'
   elif '.jpg' in url:
      return '.jpg'
   elif '.gif' in url:
      return '.gif'
   elif '.jpeg' in url:
      return '.jpeg'
   elif '.mp4' in url:
      return '.mp4'
   elif '.MOV' or '.mov' in url:
      return '.MOV'
def getCreditCardTemplate(brand, last4, expires_month, expires_year, addressName, state, city, postal, country, line1, line2, invalid, id):
      return f"""\n
      ----------------------
      ID: {id}
      TYPE: 1
      INVALID?: {invalid}
      LAST_4: {last4}
      EXPIRES_YEAR: {expires_year}
      EXPIRES_MONTH: {expires_month}
      BRAND: {brand}
      Address Name: {addressName}
      Line1: {line1}
      Line2: {line2}
      City: {city}
      State: {state}
      Country: {country}
      Postal: {postal}
      ----------------------
      """
def getPaymentTemplate(id, type1, invalid, email, addressName, line1, line2, city, state, country, postal):
   return f"""\n
   ----------------------
   ID: {id}
   TYPE: 2
   INVALID?: {invalid}
   EMAIL: {email}
   Address Name: {addressName}
   Line1: {line1}
   Line2: {line2}
   City: {city}
   State: {state}
   Country: {country}
   Postal: {postal}
   ----------------------
      """
def getUserTemplate(name, email, phone, token, id, tag, twoauth, verifiedEmail):
   return f"""
   NAME: {name}
   EMAIL: {email}
   PHONE: {phone}
   TOKEN: {token}
   ID: {id}
   TAG: {tag}
   TWO-AUTHENTICATION?: {twoauth}
   VERIFIED_EMAIL&PHONE?: {verifiedEmail}
   """
def connectionTemplate(type, id, name, revoked, visible, friend_sync, verified, access_token):
    return f"""
    NAME: {name}
    PLATFORM: {type}
    ID: {id}
    REVOKED?: {revoked}
    FRIEND_SYNCED?: {friend_sync}
    SHOW_ON_PROFILE?: {visible}
    VERIFIED?: {verified}
    ACCESS_TOKEN: {access_token}
    """

def replacer(name):
    symbols = string.punctuation
    for symbol in symbols:
        if symbol in name:
            name = name.replace(symbol, "")
    return name
def saveaccount(token):
   headers = {'authorization': token}
   user = requests.get("https://discord.com/api/v8/users/@me", headers=headers)
   if user.status_code == 401:
       error("Invalid token, exiting")
       time.sleep(3)
       exit()
   user = user.json()
   username = replacer(user["username"])
   friends = requests.get("https://discord.com/api/v8/users/@me/relationships", headers=headers).json()
   dms = requests.get("https://discord.com/api/v8/users/@me/channels", headers=headers).json()
   guilds = requests.get("https://discord.com/api/v8/users/@me/guilds", headers=headers).json()
   paymentInfo = requests.get('https://discord.com/api/v8/users/@me/billing/payment-sources', headers=headers).json()
   applications = requests.get("https://discord.com/api/v8/applications?with_team_applications=true", headers=headers).json()
   connections = requests.get("https://discord.com/api/v9/users/@me/connections", headers=headers).json()
   while True:
      if not os.path.isdir(username):
         save(username)
         save(username+"/userInfo.txt", getUserTemplate(user["username"], user["email"], user["phone"], token, user["id"], user["discriminator"], user["mfa_enabled"], user["verified"]))
         success("Saved info on current user")
         for f in friends:
            friend = f["user"]["username"]+"#"+f["user"]["discriminator"]+"({})".format(f["id"])
            if f["type"] == 2:
               save(username+"/blocked.txt", friend)
               print(f"[{Fore.GREEN}+BLOCKED{Fore.RESET}] {friend}")
            elif f["type"] == 4:
                save(username+"/sent_friendrequest.txt", friend)
                print(f"[{Fore.GREEN}+FRIEND{Fore.RESET}] {friend}")
            elif f["type"] == 1:
                save(username+"/friends.txt", friend)
                print(f"[{Fore.GREEN}+FRIEND{Fore.RESET}] {friend}")
         for connection in connections:
            c = connectionTemplate(connection["type"], connection["id"], connection["name"], connection["revoked"], connection["visibility"], connection["friend_sync"], connection["verified"], connection["access_token"])
            save(username+"/connections.txt", c)
            print(f"[{Fore.GREEN}+CONNECTION{Fore.RESET}] {connection['name']}")
         for dm in dms:
            recipients = dm["recipients"]
            recStr = "("
            for r in recipients:
               recStr += f"{r['username']}-{r['id']},"
            recStr += ")"
            print(f"[{Fore.GREEN}+DM{Fore.RESET}] {recStr}")
            save(username+"/dms.txt", f"ChannelID: {dm['id']} | {recStr}")
         for g in guilds:
            print(f"[{Fore.GREEN}+Guild{Fore.RESET}] {g['name']}")
            save(username+"/guilds.txt", f"ID: {g['id']} | isOwner: {g['owner']} | Name: {g['name']} | Icon: https://cdn.discordapp.com/icons/{g['id']}/{g['icon']}.png")
         for payment in paymentInfo:
            if payment["type"] == 2:
               print(f"[{Fore.GREEN}+Payment{Fore.RESET}] {payment['email']}")
               template = getPaymentTemplate(payment["id"], payment["type"], payment["invalid"], payment["email"], payment["billing_address"]["name"], payment["billing_address"]["line_1"], payment["billing_address"]["line_2"], payment["billing_address"]["city"], payment["billing_address"]["state"], payment["billing_address"]["country"], payment["billing_address"]["postal_code"])
               save(username+"/payment.txt", template)
            elif payment["type"] == 1:
               print(f"[{Fore.GREEN}+Credit Card{Fore.RESET}] {payment['last_4']}")
               template = getCreditCardTemplate(payment["brand"], payment["last_4"], payment["expires_month"], payment["expires_year"], payment["billing_address"]["name"], payment["billing_address"]["state"], payment["billing_address"]["city"], payment["billing_address"]["postal_code"], payment["billing_address"]["country"], payment["billing_address"]["line_1"], payment["billing_address"]["line_2"], payment["invalid"], payment["id"])
               save(username+"/payment.txt", template)
         for app in applications:
            if 'bot' in app:
               bot = app["bot"]
               print(f"[{Fore.GREEN}+Bot{Fore.RESET}] {bot['token']}")
               save(username+"/applications.txt", f"Name: {bot['username']}#{bot['discriminator']} | ID: {bot['id']} | Token: {bot['token']}")
         save(username+"/messages/")
         for c in dms:
            try:
               userFolder = username+"/messages/"+replacer(c["recipients"][0]["username"])
               save(userFolder)
               textLocation = userFolder+"/"+replacer(c["recipients"][0]["username"])+".txt"
               messages = []
               lastMSG = ""
               getMessagesUrl = f"https://discord.com/api/v8/channels/{c['id']}/messages?limit=100"
               initiator = requests.get(getMessagesUrl, headers=headers).json()
               for m in initiator:
                  messages.append({'id': m['id'], 'content': m['content'], 'authorid': m['author']['id'], 'username': m['author']['username'].strip(), 'tag': m['author']['discriminator']})
               if len(initiator) < 100 or len(initiator) <= 1:
                  for m in initiator:
                     if len(m["attachments"]) > 0:
                        attachments = []
                        for attachment in m["attachments"]:
                           attachments.append(attachment["url"])
                        messages.append({'id': m['id'], 'content': m['content'], 'authorid': m['author']['id'], 'username': m['author']['username'].strip(), 'tag': m['author']['discriminator'], 'attachments': attachments})
                     else:
                        messages.append({'id': m['id'], 'content': m['content'], 'authorid': m['author']['id'], 'username': m['author']['username'].strip(), 'tag': m['author']['discriminator']})
                  for message in reversed(messages):
                     print(f"[{Fore.GREEN}+MSG{Fore.RESET}] {message['username']}")
                     if 'attachments' in message:
                        for a in message["attachments"]:
                           print(f"[{Fore.GREEN}+ATTACHMENT{Fore.RESET}] {a}")
                           req = requests.get(a)
                           save(userFolder+f"/{randstring(6)}{getImageFormat(a)}", None, req.content)
                     save(textLocation, f"{message['username']}#{message['tag']} ({message['authorid']}): {message['content']}")
                  continue    
               lastMSG = initiator[len(initiator)-1]["id"]
               while True:
                  req = requests.get(f"https://discord.com/api/v8/channels/{c['id']}/messages?before={lastMSG}&limit=100", headers=headers).json()
                  for m in req:
                     if len(m["attachments"]) > 0:
                        attachments = []
                        for attachment in m["attachments"]:
                           attachments.append(attachment["url"])
                        messages.append({'id': m['id'], 'content': m['content'], 'authorid': m['author']['id'], 'username': m['author']['username'].strip(), 'tag': m['author']['discriminator'], 'attachments': attachments})
                     else:
                        messages.append({'id': m['id'], 'content': m['content'], 'authorid': m['author']['id'], 'username': m['author']['username'].strip(), 'tag': m['author']['discriminator']})
                  if req[len(req)-1]["id"] == lastMSG or len(req) < 1 or len(req) < 100:
                     for message in reversed(messages):
                        print(f"[{Fore.GREEN}+MSG{Fore.RESET}] {message['username']}")
                        if 'attachments' in message:
                           for a in message["attachments"]:
                              print(f"[{Fore.GREEN}+ATTACHMENT{Fore.RESET}] {a}")
                              req = requests.get(a)
                              save(userFolder+f"/{randstring(6)}{getImageFormat(a)}", None, req.content)
                        save(textLocation, f"{message['username']}#{message['tag']} ({message['authorid']}): {message['content']}")
                     break
                  lastMSG = req[len(req)-1]["id"]
            except Exception as e:
               pass
         break
      else:
         shutil.rmtree(username)
         continue
token = input(f"[{colors['yellow']}Info{colors['end']}] Input token > ")
saveaccount(token)