Q# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# D3VIL UserBot - D3KRISH

""" UserBot starting point """
import importlib
from importlib import import_module
from sqlite3 import connect
import os
import requests
from telethon.tl.types import InputMessagesFilterDocument
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
from telethon.tl.functions.channels import GetMessagesRequest
from . import BRAIN_CHECKER, LOGS, bot, PLUGIN_CHANNEL_ID, CMD_HELP, LANGUAGE, ASENA_VERSION, PATTERNS
from .modules import ALL_MODULES
import userbot.modules.sql_helper.mesaj_sql as MSJ_SQL
import userbot.modules.sql_helper.galeri_sql as GALERI_SQL
from pySmartDL import SmartDL
from telethon.tl import functions

from random import choice
import chromedriver_autoinstaller
from json import loads, JSONDecodeError
import re
import userbot.cmdhelp

SEWING_STR = [
    "I'm editing the sticker ...",
    "Long live ordering ...",
    "I invite this sticker to my package ...",
    "I have to fix this ...",
    "Hey this is a nice sticker! \ NI'm just squeaking ..",
    "I'm flattening your sticker \ nhahaha.",
    "Hey look over there. (☉｡☉)! → \ n While I was editing this ...",
    "Roses red violets blue, I'll be cool by putting this sticker on my pack ...",
    "Sticker is imprisoned ...",
    "Mister stunner pranks this sticker ...",
]

AFKSTR = [
    "I'm in a rush right now, can't you send me a message later? I'll be back anyway.",
    "The person you are calling cannot answer the phone right now. You can leave your message on your own tariff after the tone. The message costs 49 kurus. \ N`biiiiiiiiiiiiiiiiiiiiiiiiiiip`!",
    "I'll be back in a few minutes. But if I don't ... wait longer.",
    "I'm not here right now, I'm probably somewhere else.",
    "Roses are red \ nOns are blue \ nLeave me a message \ nAnd I'll get back to you.",
    "Sometimes the best things in life are worth the wait… \ nI'll be right back.",
    "I'll be right back, but if I don't come back, I'll be back later.",
    "If you don't get it yet, I'm not here.",
    "Hello, welcome to my distant message, how can I ignore you today?",
    "I am away from 7 seas and 7 countries, \ n7 water and 7 continents, \ n7 mountains and 7 hills, \ n7 plain and 7 mounds, \ n7 pools and 7 lakes, \ n7 spring and 7 meadows, \ n7 cities and 7 neighborhoods, \ n7 blocks and 7 houses ... \ n \ nWhere even messages can't reach me! ",
    "I'm away from the keyboard right now, but if you scream loud enough on your screen, I can hear you.",
    "I'm moving in the following direction \ n ---->",
    "I'm moving in the following direction \ n <----",
    "Please leave a message and make me feel more important than I already am.",
    "My owner is not here, so stop writing to me.",
    "If I were here, \ nI would tell you where I am. \ N \ nBut it's not me, \ when I come back ask me ...",
    "I'm away! \ NI don't know when I'll be back! \ NI hope a few minutes later!",
    "My owner is not available right now. If you give him your name, number and address, I can send it to him and so when he comes back.",
    "Sorry, my owner is not here. You can talk to me until he arrives. \ NThe owner will return to you later.",
    "I bet you were expecting a message!",
    "Life is too short, there are so many things to do ... \ nI am doing one of them ...",
    "I'm not here right now .... \ n but if I am ... \ n \ n wouldn't that be great?",
]

UNAPPROVED_MSG = ('' Hey, `{mention}`! This is a bot. Don't worry. \ N \ n` "
                  `` My owner hasn't given you permission to PM. ''
                  "Please wait for my owner to be active, he will usually confirm PMs. \ N \ n`"
                  "As far as I know, he doesn't allow people to PM in a nutshell.")

DB = connect ("learning-data-root.check")
CURSOR = DB.cursor ()
CURSOR.execute ("" "SELECT * FROM BRAIN1" "")
ALL_ROWS = CURSOR.fetchall ()
INVALID_PH = '\ nERROR: The phone number entered is invalid' \
             '\ n Hint: Enter your number using your country code' \
             '\ n Check your phone number again'

for i in ALL_ROWS:
    BRAIN_CHECKER.append (i [0])
connect ("learning-data-root.check"). close ()

def extractCommands (file):
    FileRead = open (file, 'r'). Read ()
    
    if '/' in file:
        file = file.split ('/') [- 1]

    Pattern = re.findall (r "@register \ (. * Pattern = (r |) \" (. *) \ ". * \)", FileRead)
    Commands = []

    if re.search (r'CmdHelp \ (. * \) ', FileRead):
        pass
    else:
        fileName = file.replace ('. py', '')
        CmdHelp = userbot.cmdhelp.CmdHelp (fileName, False)

        # We Receive Commands #
        for Command in Pattern:
            Command = Command [1]
            if Command == '' or len (Command) <= 1:
                continue
            Command = re.findall ("(^. * [A-zA-Z0-9 light] \ w)", Command)
            if (len (Command)> = 1) and (not Command [0] == ''):
                Command = Command [0]
                if Command [0] == '^':
                    CommandStr = Command [1:]
                    if CommandStr [0] == '.':
