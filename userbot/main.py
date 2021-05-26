# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta

""" UserBot başlangıç noktası """
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

DIZCILIK_STR = [
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

UNAPPROVED_MSG = ("`Hey, `{mention}`! This is a bot. Don't worry. \ N \ n` "
                  "` My owner hasn't given you permission to PM. `"
                  "`Please wait for my owner to be active, he will usually confirm PM.\n\n`"
                  "`As far as I know, he doesn't allow people to PM in a nutshell.`")

DB = connect("learning-data-root.check")
CURSOR = DB.cursor()
CURSOR.execute("""SELECT * FROM BRAIN1""")
ALL_ROWS = CURSOR.fetchall()
INVALID_PH = '\nERROR: The phone number entered is invalid' \
             '\n  Hint: Enter your number using your country code' \
             '\n     Check your phone number again'

for i in ALL_ROWS:
    BRAIN_CHECKER.append(i[0])
connect("learning-data-root.check").close()

def extractCommands(file):
    FileRead = open(file, 'r').read()
    
    if '/' in file:
        file = file.split('/')[-1]

    Pattern = re.findall(r"@register\(.*pattern=(r|)\"(.*)\".*\)", FileRead)
    Komutlar = []

    if re.search(r'CmdHelp\(.*\)', FileRead):
        pass
    else:
        dosyaAdi = file.replace('.py', '')
        CmdHelp = userbot.cmdhelp.CmdHelp(dosyaAdi, False)

        # Komutları Alıyoruz #
        for Command in Pattern:
            Command = Command[1]
            if Command == '' or len(Command) <= 1:
                continue
            Komut = re.findall("(^.*[a-zA-Z0-9şğüöçı]\w)", Command)
            if (len(Komut) >= 1) and (not Komut[0] == ''):
                Komut = Komut[0]
                if Komut[0] == '^':
                    KomutStr = Komut[1:]
                    if KomutStr[0] == '.':
                        KomutStr = KomutStr[1:]
                    Komutlar.append(KomutStr)
                else:
                    if Command[0] == '^':
                        KomutStr = Command[1:]
                        if KomutStr[0] == '.':
                            KomutStr = KomutStr[1:]
                        else:
                            KomutStr = Command
                        Komutlar.append(KomutStr)

            # AsenaPY
            Asenapy = re.search('\"\"\"ASENAPY(.*)\"\"\"', FileRead, re.DOTALL)
            if not Asenapy == None:
                Asenapy = Asenapy.group(0)
                for Satir in Asenapy.splitlines():
                    if (not '"""' in Satir) and (':' in Satir):
                        Satir = Satir.split(':')
                        Isim = Satir[0]
                        Deger = Satir[1][1:]
                                
                        if Isim == 'INFO':
                            CmdHelp.add_info(Deger)
                        elif Isim == 'WARN':
                            CmdHelp.add_warning(Deger)
                        else:
                            CmdHelp.set_file_info(Isim, Deger)
            for Komut in Komutlar:
                # if re.search('\[(\w*)\]', Komut):
                    # Komut = re.sub('(?<=\[.)[A-Za-z0-9_]*\]', '', Komut).replace('[', '')
                CmdHelp.add_command(Komut, None, 'This plugin has been installed externally. No explanation has been defined.')
            CmdHelp.add()

try:
    bot.start()
    idim = bot.get_me().id
    asenabl = requests.get('https://gitlab.com/Quiec/asen/-/raw/master/asen.json').json()
    if idim in asenabl:
        bot.disconnect()

    # ChromeDriver'ı Ayarlayalım #
    try:
        chromedriver_autoinstaller.install()
    except:
        pass
    
    # Galeri için değerler
    GALERI = {}

    # PLUGIN MESAJLARI AYARLIYORUZ
    PLUGIN_MESAJLAR = {}
    ORJ_PLUGIN_MESAJLAR = {"alive": "`⚔️ D3VILUSERBOT IS ALIVE ⚔️", "afk": f"`{str(choice(AFKSTR))}`", "kickme": "`Goodbye i'm going `🤠", "pm": UNAPPROVED_MSG, "stop": str(choice(DIZCILIK_STR)), "ban": "{mention}`, banned!`", "mute": "{mention}`, muted!`", "approve": "{mention}`, now you can send me a message!`", "disapprove": "{mention}`, now you can't message me because I disapprove yo you!`", "block": "{mention}`, blocked!`"}

    PLUGIN_MESAJLAR_TURLER = ["alive", "afk", "kickme", "pm", "stop", "ban", "mute", "approve", "disapprove", "block"]
    for mesaj in PLUGIN_MESAJLAR_TURLER:
        dmsj = MSJ_SQL.getir_mesaj(mesaj)
        if dmsj == False:
            PLUGIN_MESAJLAR[mesaj] = ORJ_PLUGIN_MESAJLAR[mesaj]
        else:
            if dmsj.startswith("MEDIA_"):
                medya = int(dmsj.split("MEDIA_")[1])
                medya = bot.get_messages(PLUGIN_CHANNEL_ID, ids=media)

                PLUGIN_MESAJLAR[mesaj] = media
            else:
                PLUGIN_MESAJLAR[mesaj] = dmsj
    if not PLUGIN_CHANNEL_ID == None:
        LOGS.info("Plugins Loading")
        try:
            KanalId = bot.get_entity(PLUGIN_CHANNEL_ID)
        except:
            KanalId = "me"

        for plugin in bot.iter_messages(KanalId, filter=InputMessagesFilterDocument):
            if plugin.file.name and (len(plugin.file.name.split('.')) > 1) \
                and plugin.file.name.split('.')[-1] == 'py':
                Split = plugin.file.name.split('.')

                if not os.path.exists("./userbot/modules/" + plugin.file.name):
                    dosya = bot.download_media(plugin, "./userbot/modules/")
                else:
                    LOGS.info("This Plugin is Already Installed " + plugin.file.name)
                    extractCommands('./userbot/modules/' + plugin.file.name)
                    dosya = plugin.file.name
                    continue 
                
                try:
                    spec = importlib.util.spec_from_file_location("userbot.modules." + Split[0], dosya)
                    mod = importlib.util.module_from_spec(spec)

                    spec.loader.exec_module(mod)
                except Exception as e:
                    LOGS.info(f"`Upload failed! Plugin is faulty.\n\nHata: {e}`")

                    try:
                        plugin.delete()
                    except:
                        pass

                    if os.path.exists("./userbot/modules/" + plugin.file.name):
                        os.remove("./userbot/modules/" + plugin.file.name)
                    continue
                extractCommands('./userbot/modules/' + plugin.file.name)
    else:
        bot.send_message("me", f"`Please ensure that plugins are permanent PLUGIN_CHANNEL_ID'i set up.`")
except PhoneNumberInvalidError:
    print(INVALID_PH)
    exit(1)

async def FotoDegistir (foto):
    FOTOURL = GALERI_SQL.TUM_GALERI[foto].foto
    r = requests.get(FOTOURL)

    with open(str(foto) + ".jpg", 'wb') as f:
        f.write(r.content)    
    file = await bot.upload_file(str(foto) + ".jpg")
    try:
        await bot(functions.photos.UploadProfilePhotoRequest(
            file
        ))
        return True
    except:
        return False

for module_name in ALL_MODULES:
    imported_module = import_module("userbot.modules." + module_name)

LOGS.info("Your D3VIL bot is running! Test it by typing .alive in any chat."
          " If you need help, come to our Support group t.me/D3VIL_SUPPORT")
LOGS.info(f"Your bot version: D3vil {ASENA_VERSION}")

"""
if len(argv) not in (1, 3, 4):
    bot.disconnect()
else:
"""
bot.run_until_disconnected()
