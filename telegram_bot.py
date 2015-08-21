""" The main interface of the Telegram Bot, where all methods are defined
TODO: 
    try-catch everything 
    comment every function
    save token externally (safer than hardcoded ones)
    a nice central interface (with possibility to use more bots)
    beautiful code"""

import json
import requests
from telegram_utility import (GetParameter, DeJson, MyError, PrintDict, GetFormat, ReadOffset, WriteOffset)
from telegram_types import (TelegramObject,User, GroupChat, Message, PhotoSize, Audio, Document, Sticker, Video, Voice, Contact, Location, Update, UserProfilePhotos, ReplyKeyboardHide, ReplyKeyboardMarkup, ForceReply )
from requests_toolbelt import MultipartEncoder

TIMEOUT = 2

class Bot(object):
    
    def __init__(self, token):
        self.bot_token = token
        self.bot_request_url = "https://api.telegram.org/bot"+self.bot_token+"/"
        print("           ***** Welcome to the Telegram Bot Carlo's Interface *****\n\n\n")
        user_dict = self.getMe().user_dict
        PrintDict(user_dict)
        self.bot_username = user_dict["first_name"]
        
    # Starts receiving updates (via short/long polling) until manually interrupted, to be called only once
    
    def StartPolling(self):
        last_update = ReadOffset("offset.txt")
        while True:
            upd_arr = self.getUpdate({"offset":last_update, "timeout":TIMEOUT})
            f = False
            for i in upd_arr:
                last_update = max(last_update, i.update_update_id)
                
                recv_message = i.update_message
                recv_message.Debug(recv_message.message_dict, str( type(recv_message) ))
                
                sender = User( GetParameter(recv_message.message_dict,"from") ).user_dict
                sender_id = GetParameter(sender, "id")
                
                """ Echo Bot: """
                if i.update_update_id >= last_update:
                    self.sendMessage({"chat_id":sender_id, "text": GetParameter(recv_message.message_dict, "text", True)})
                    f = True
                   
                print("...Done\n\n")
            
            WriteOffset("offset.txt", last_update)
            if f:
                last_update += 1
    
    # Gets a list of updates with id > offset
    
    def getUpdate(self, getupd_dict):
        try:
            url = self.bot_request_url + "getUpdates"
            upd_arr = self.Execute(url, params=getupd_dict)
            return [Update(i) for i in upd_arr]
        except:
            raise MyError("Unable to retrieve updates")
            
    # Returns bot's id, name and username in a User object
    
    def getMe(self):
        try:
            me_dict = self.Execute(self.bot_request_url+"getMe")
            return User( me_dict )
        except:
            raise MyError("Unable to getMe")
    
    # Sends a text Message object to User/GroupChat and, in case of success, returns the Message sent
    
    def sendMessage(self, send_dict):
        try:
            url = self.bot_request_url + "sendMessage" 
            message_dict = self.Execute(url, params=send_dict)
            return Message( message_dict )
        except:
            raise MyError("Unable to send the message")
    
    # Forwards a Message to User/GroupChat and, in case of success, returns the message forwarded
    
    def forwardMessage(self, forward_dict):
        try:
            url = self.bot_request_url + "forwardMessage"
            message_dict = self.Execute(url, params=forward_dict)
            return Message( message_dict )
        except:
            raise MyError("Unable to forward the message")
     
    #Sends a photo and, in case of success, returns the message sent
    
    def sendPhoto(self, param_dict, photo_path):
        try:
            header = "image/" + GetFormat(photo_path, ".")
            filename = GetFormat(photo_path, "/")   
            m = MultipartEncoder( fields = {"photo" : (filename, open(photo_path, "rb"), header)} )
            tmp_message = self.Execute(self.bot_request_url+"sendPhoto", params=param_dict, data=m, headers={"Content-Type":m.content_type})
            return Message( tmp_message )
        except:
            raise MyError("Unable to send photo")
       
    # Sends an .mp3 audio and, in case of success, returns the message sent
         
    def sendAudio(self, param_dict, audio_path):
        try:
            header = "audio/mpeg"
            filename = GetFormat(audio_path, "/")   
            m = MultipartEncoder( fields = {"audio" : (filename, open(audio_path, "rb"), header)} )
            tmp_message = self.Execute(self.bot_request_url+"sendAudio", params=param_dict, data=m, headers={"Content-Type":m.content_type})
            return Message( tmp_message )
        except:
            raise MyError("Unable to send audio")
    
    # Sends a .ogg [ encoded with OPUS ] voice and, in case of success, returns the message sent
         
    def sendVoice(self, param_dict, voice_path):
        try:
            header = "audio/ogg"
            filename = GetFormat(voice_path, "/")   
            m = MultipartEncoder( fields = {"voice" : (filename, open(voice_path, "rb"), header)} )
            tmp_message = self.Execute(self.bot_request_url+"sendVoice", params=param_dict, data=m, headers={"Content-Type":m.content_type})
            return Message( tmp_message )
        except:
            raise MyError("Unable to send voice")
    
    # Sends a text/plain document and, in case of success, returns the message sent
    
    def sendDocument(self, param_dict, document_path):
        try:
            header = "text/plain"
            filename = GetFormat(document_path, "/")   
            m = MultipartEncoder( fields = {"document" : (filename, open(document_path, "rb"), header)} )
            tmp_message = self.Execute(self.bot_request_url+"sendDocument", params=param_dict, data=m, headers={"Content-Type":m.content_type})
            return Message( tmp_message )
        except:
            raise MyError("Unable to send document")
    
    # Sends a .webp sticker and, in case of success, returns the message sent
    
    def sendSticker(self, param_dict, sticker_path):
        try:
            header = "image/webp"
            filename = GetFormat(sticker_path, "/")   
            m = MultipartEncoder( fields = {"sticker" : (filename, open(sticker_path, "rb"), header)} )
            tmp_message = self.Execute(self.bot_request_url+"sendSticker", params=param_dict, data=m, headers={"Content-Type":m.content_type})
            return Message( tmp_message )
        except:
            raise MyError("Unable to send sticker")
    
    # Sends a .mp4 video and, in case of success, returns the message sent
    
    def sendVideo(self, param_dict, video_path):
        try:
            header = "video/mp4"
            filename = GetFormat(video_path, "/")   
            m = MultipartEncoder( fields = {"video" : (filename, open(video_path, "rb"), header)} )
            tmp_message = self.Execute(self.bot_request_url+"sendVideo", params=param_dict, data=m, headers={"Content-Type":m.content_type})
            return Message( tmp_message )
        except:
            raise MyError("Unable to send video")
        
                    
    # Sends the location and, in case of success, returns the message sent
    
    def sendLocation(self, location_dict):
        try:
            url = self.bot_request_url + "sendLocation" 
            tmp_dict = self.Execute(url, location_dict)
            return Message( tmp_dict )
        except:
            raise MyError("Unable to send the location")
        
    # Sends the chat action (e.g. 'typing', 'sending a photo' etc)
    
    def sendChatAction(self, chat_dict):
        try:
            url = self.bot_request_url + "sendChatAction"
            self.Execute(url, params=chat_dict)
        except:
            raise MyError("Unable to send chat action")
        
    # Executes a request to a specified url and returns a dict   
    
    def Execute(self, url, params=None, data=None, headers=None):
        r = requests.post(url, params=params, data=data, headers=headers)
        if r.status_code != requests.codes.ok:
            raise MyError("Unable to execute the post request") 
        
        tmp_dict = r.json()
        if ("ok" not in tmp_dict) or (GetParameter(tmp_dict, "ok")==False):
            raise MyError("Bad request") 
        else:
            return GetParameter(tmp_dict, "result")
        
        
