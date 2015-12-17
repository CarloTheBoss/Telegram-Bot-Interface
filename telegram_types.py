""" A list of the standard types listed in the Telegram official API
 Every type can only be initialized with a dict (that must be already de-jsoned)
 In every type, optional attributes can be omitted, but an exception is raised if some fundamental attribute is missing
 Standard attribute names are declared like this:
    Class Example:
        self.example_name_of_attribute = bla bla
 Attribute names are the same of the official Telegram API """
 
from telegram_utility import (GetParameter,ToJson)


""" Every class has a dict of all of his attributes and a nameclass_json which contains a json serialized string of the class """

class TelegramObject(object):
    def __init__(self):
        pass
    
    def Debug(self, tmp_dict, obj_name):
        print("\n\n"+obj_name+" debug:\n")
        for i in tmp_dict:
            print(str(i) + " : " + str(tmp_dict[i]))
        print("\n\n")

class User(TelegramObject):
    def __init__(self, user_dict):
        self.user_dict = user_dict
        self.user_json = ToJson(user_dict) 

class GroupChat(TelegramObject):
    def __init__(self, groupchat_dict):
        self.groupchat_dict = groupchat_dict
        self.groupchat_json = ToJson(groupchat_dict) 

        
class PhotoSize(TelegramObject):
    def __init__(self, photosize_dict):
        self.photosize_dict = photosize_dict
        self.photosize_json = ToJson(photosize_dict) 

        
class Audio(TelegramObject):
    def __init__(self, audio_dict):
        self.audio_dict = audio_dict
        self.audio_json = ToJson(audio_dict)
    
class Document(TelegramObject):
    def __init__(self, document_dict):
        self.document_dict = document_dict
        self.document_json = ToJson(document_dict)
        
class Sticker(TelegramObject):
    def __init__(self, sticker_dict):
        self.sticker_dict = sticker_dict
        self.sticker_json = ToJson(sticker_dict)

class Video(TelegramObject):
    def __init__(self, video_dict):
        self.video_dict = video_dict
        self.video_json = ToJson(video_dict)

class Voice(TelegramObject):
    def __init__(self, voice_dict):
        self.voice_dict = voice_dict
        self.voice_json = ToJson(voice_dict)

class Contact(TelegramObject):
    def __init__(self, contact_dict):
        self.contact_dict = contact_dict
        self.contact_json = ToJson(contact_dict)

class Location(TelegramObject):
    def __init__(self, location_dict):
        self.location_dict = location_dict
        self.location_json = ToJson(location_dict)
        
class UserProfilePhotos(TelegramObject):
    def __init__(self, userprofilephotos_dict):
        self.userprofilephotos_dict = userprofilephotos_dict
        self.userprofilephotos_json = ToJson(userprofilephotos_dict)
            
class ReplyKeyboardMarkup(TelegramObject):
    def __init__(self, replykeyboardmarkup_dict):
        self.replykeyboardmarkup_dict = replykeyboardmarkup_dict
        self.replykeyboardmarkup_json = ToJson(replykeyboardmarkup_dict)
    
class ReplyKeyboardHide(TelegramObject):
    def __init__(self, replykeyboardhide_dict):
        self.replykeyboardhide_dict = replykeyboardhide_dict
        self.replykeyboardhide_json = ToJson(replykeyboardhide_dict)
    
class ForceReply(TelegramObject):
    def __init__(self, forcereply_dict):
        self.forcereply_dict = forcereply_dict
        self.forcereply_json = ToJson(forcereply_dict)
    
class Message(TelegramObject):
    def __init__(self, message_dict):
        self.message_dict = message_dict
        self.message_json = ToJson(message_dict)

class Update(TelegramObject):
    def __init__(self, update_dict):
        self.update_update_id = GetParameter(update_dict, "update_id")
        self.update_message = Message( GetParameter(update_dict, "message", True) )
   
