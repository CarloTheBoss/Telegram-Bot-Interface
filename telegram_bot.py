""" The main interface of the Telegram Bot, where all methods are defined """

import json
import requests
import os
from telegram_utility import (GetParameter, DeJson, MyError, PrintDict, GetFormat, ReadOffset, WriteOffset)
from telegram_types import (TelegramObject,User, GroupChat, Message, PhotoSize, Audio, Document, Sticker, Video, Voice, Contact, Location, Update, UserProfilePhotos, ReplyKeyboardHide, ReplyKeyboardMarkup, ForceReply )
from requests_toolbelt import MultipartEncoder

# Standard timeout for polling updates.

TIMEOUT = 2


class Bot(object):
    
    # Bot is initialized.
    # @token -> bot's token to access API.
    
    def __init__(self, token):
        try:
            os.system("clear")
            self.bot_token = token
            self.bot_request_url = "https://api.telegram.org/bot"+self.bot_token+"/"
            print("           ***** Welcome to the Telegram Bot Carlo's Interface *****\n\n\n")
            PrintDict(self.getMe().user_dict)
        except:
            raise MyError("Unable to init the bot")
        
    # Starts receiving updates (via short/long polling) until manually interrupted, to be called only once.
    # Last update offset is saved in the 'offset.txt' file.
    # @HandleMessage -> function to call when handling a message. It must return the last update offset. His args are [last update offset, Update].
    # @time -> the time of polling. If None, TIMEOUT will be used.
    
    def StartPolling(self, HandleMessage, time=TIMEOUT):       
        last_update = ReadOffset("offset.txt")
        while True:
            
            upd_arr = self.getUpdate({"offset":last_update, "timeout":time})
            f = False
            
            for i in upd_arr:
                
                if last_update <= i.update_update_id:
                    WriteOffset("offset.txt", i.update_update_id+1)
                    f = True
                    last_update = max(last_update, HandleMessage(last_update, i))
                    
            if f:
                last_update += 1
            
            WriteOffset("offset.txt", last_update)
    
    # Gets a list of updates with id > offset.
    # @getupd_dict -> dict with parameters to use (see Telegram API)
    
    def getUpdate(self, getupd_dict):
        try:
            url = self.bot_request_url + "getUpdates"
            upd_arr = self.Execute(url, params=getupd_dict)
            return [Update(i) for i in upd_arr]
        except:
            raise MyError("Unable to retrieve updates")
            
    # Returns bot's id, name and username in a User object.
    
    def getMe(self):
        try:
            me_dict = self.Execute(self.bot_request_url+"getMe")
            return User( me_dict )
        except:
            raise MyError("Unable to getMe")
    
    # Sends a text Message object to User/GroupChat and, in case of success, returns the Message sent.
    # @send_dict -> dict with parameters to use (see Telegram API)
    
    def sendMessage(self, send_dict):
        try:
            url = self.bot_request_url + "sendMessage" 
            message_dict = self.Execute(url, params=send_dict)
            return Message( message_dict )
        except:
            raise MyError("Unable to send the message")
    
    # Forwards a Message to User/GroupChat and, in case of success, returns the message forwarded.
    # @forward_dict -> dict with parameters to use (see Telegram API)
    
    def forwardMessage(self, forward_dict):
        try:
            url = self.bot_request_url + "forwardMessage"
            message_dict = self.Execute(url, params=forward_dict)
            return Message( message_dict )
        except:
            raise MyError("Unable to forward the message")
     
    #Sends a photo and, in case of success, returns the message sent.
    # @param_dict -> dict with parameters to use (see Telegram API)
    # @photo_path -> the path of the photo
    
    def sendPhoto(self, param_dict, photo_path):
        try:
            header = "image/" + GetFormat(photo_path, ".")
            filename = GetFormat(photo_path, "/")   
            m = MultipartEncoder( fields = {"photo" : (filename, open(photo_path, "rb"), header)} )
            tmp_message = self.Execute(self.bot_request_url+"sendPhoto", params=param_dict, data=m, headers={"Content-Type":m.content_type})
            return Message( tmp_message )
        except:
            raise MyError("Unable to send photo")
       
    # Sends an .mp3 audio and, in case of success, returns the message sent.
    # @param_dict -> dict with parameters to use (see Telegram API)
    # @audio_path -> the path of the audio  
    
    def sendAudio(self, param_dict, audio_path):
        try:
            header = "audio/mpeg"
            filename = GetFormat(audio_path, "/")   
            m = MultipartEncoder( fields = {"audio" : (filename, open(audio_path, "rb"), header)} )
            tmp_message = self.Execute(self.bot_request_url+"sendAudio", params=param_dict, data=m, headers={"Content-Type":m.content_type})
            return Message( tmp_message )
        except:
            raise MyError("Unable to send audio")
    
    # Sends a .ogg [ encoded with OPUS ] voice and, in case of success, returns the message sent.
    # @param_dict -> dict with parameters to use (see Telegram API)
    # @voice_path -> the path of the voice
    
    def sendVoice(self, param_dict, voice_path):
        try:
            header = "audio/ogg"
            filename = GetFormat(voice_path, "/")   
            m = MultipartEncoder( fields = {"voice" : (filename, open(voice_path, "rb"), header)} )
            tmp_message = self.Execute(self.bot_request_url+"sendVoice", params=param_dict, data=m, headers={"Content-Type":m.content_type})
            return Message( tmp_message )
        except:
            raise MyError("Unable to send voice")
    
    # Sends a text/plain document and, in case of success, returns the message sent.
    # @param_dict -> dict with parameters to use (see Telegram API)
    # @document_path -> the path of the document
    
    def sendDocument(self, param_dict, document_path):
        try:
            header = "text/plain"
            filename = GetFormat(document_path, "/")   
            m = MultipartEncoder( fields = {"document" : (filename, open(document_path, "rb"), header)} )
            tmp_message = self.Execute(self.bot_request_url+"sendDocument", params=param_dict, data=m, headers={"Content-Type":m.content_type})
            return Message( tmp_message )
        except:
            raise MyError("Unable to send document")
    
    # Sends a .webp sticker and, in case of success, returns the message sent.
    # @param_dict -> dict with parameters to use (see Telegram API)
    # @sticker_path -> the path of the sticker
    
    def sendSticker(self, param_dict, sticker_path):
        try:
            header = "image/webp"
            filename = GetFormat(sticker_path, "/")   
            m = MultipartEncoder( fields = {"sticker" : (filename, open(sticker_path, "rb"), header)} )
            tmp_message = self.Execute(self.bot_request_url+"sendSticker", params=param_dict, data=m, headers={"Content-Type":m.content_type})
            return Message( tmp_message )
        except:
            raise MyError("Unable to send sticker")
    
    # Sends a .mp4 video and, in case of success, returns the message sent.
    # @param_dict -> dict with parameters to use (see Telegram API)
    # @video_path -> the path of the video
    
    def sendVideo(self, param_dict, video_path):
        try:
            header = "video/mp4"
            filename = GetFormat(video_path, "/")   
            m = MultipartEncoder( fields = {"video" : (filename, open(video_path, "rb"), header)} )
            tmp_message = self.Execute(self.bot_request_url+"sendVideo", params=param_dict, data=m, headers={"Content-Type":m.content_type})
            return Message( tmp_message )
        except:
            raise MyError("Unable to send video")
        
                    
    # Sends the location and, in case of success, returns the message sent.
    # @location_dict -> dict with parameters to use (see Telegram API)
    
    def sendLocation(self, location_dict):
        try:
            url = self.bot_request_url + "sendLocation" 
            tmp_dict = self.Execute(url, location_dict)
            return Message( tmp_dict )
        except:
            raise MyError("Unable to send the location")
        
    # Sends the chat action (e.g. 'typing', 'sending a photo' etc).
    # @chat_dict -> dict with the parameters to use (see Telegram API)
    
    def sendChatAction(self, chat_dict):
        try:
            url = self.bot_request_url + "sendChatAction"
            self.Execute(url, params=chat_dict)
        except:
            raise MyError("Unable to send chat action")
        
    # Executes a request to a specified url and returns a dict.
    # @url -> url to send the post request to
    # @params -> dict with Json parameters to encode in url query string
    # @data -> data to send with multipart-form data
    # @headers -> optional headers.
    
    def Execute(self, url, params=None, data=None, headers=None):
        try:
            r = requests.post(url, params=params, data=data, headers=headers)
            if r.status_code != requests.codes.ok:
                raise MyError("Unable to execute the post request") 
            
            tmp_dict = r.json()
            if ("ok" not in tmp_dict) or (GetParameter(tmp_dict, "ok")==False):
                raise MyError("Bad request") 
            else:
                return GetParameter(tmp_dict, "result")
        except:
            raise MyError("Unable to execute the post request")
        
        
