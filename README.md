# Telegram-Bot-Interface
A simple telegram bot interface written in Python3.
There are 3 different modules:

      .Telegram_bot: The main module, where Bot class and all his methods are defined. The only thing you have to do is write your own HandleMessage and call the StartPolling function!
      .Telegram_types: All types available in Telegram Bot API are defined and contain a dict with all parameters and a json string of it.
      .Telegram_utility: A bunch of useful functions, like GetParameters or JSON encoder/decoder.

Check dev_requirements.txt for all external python modules used in this project.
