#! /usr/bin/env python


from smartcard.Exceptions import NoCardException
from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.Exceptions import CardConnectionException
from smartcard.System import readers
from smartcard.util import toHexString
import asyncio
import keyboard
import ahk
import os
import subprocess 
global imagen
global autohotkey
try:                                                                                                                                                                         
    autohotkey = ahk.AHK(executable_path="C:\\Program Files\\AutoHotkey\\AutoHotkeyU64.exe")                                                                                                                                                                           
except:                                                                                                                                                                         
    autohotkey = ahk.AHK(executable_path="C:\\Program Files\\AutoHotkey\\AutoHotkeyU32.exe")



class ObservaTarjeta(CardObserver):
    """A simple card observer that is notified
    when cards are inserted/removed from the system and
    prints the list of cards
    """
    def update(self, observable, actions):
        (addedcards, removedcards) = actions
        for card in addedcards:
            comprobador(card)
        for card in removedcards:
            for i in range(150):
                keyboard.block_key(i)

            autohotkey.run_script('BlockInput,MouseMove', blocking=False)
            print("Bloqueando ")            
            imagen = subprocess.Popen(['i_view64.exe','FondoV2.png', '/fs'])

def comprobador(card):
    ATR=toHexString(card.atr)
    ATR=Replace(ATR)

    if (ATR == "3B6F0000806645460138180353023124829000" or 
        ATR == "3B6800008066A20308013107" or 
        ATR == "3B6F0000806645460138180353023110829000" or 
        ATR == "3B6F00008066B0070101770753023110829000"):
        for i in range(150):
            keyboard.unblock_key(i)
        os.system("taskkill /f /im  AutoHotKeyU64.exe")
        os.system("taskkill /f /im  AutoHotkeyU32.exe")
        print("Desbloqueando ")
        imagen.terminate()



def Replace(String):
    String = String.replace(" ","")
    return String

for i in range(150):
   keyboard.block_key(i)
   
autohotkey.run_script('BlockInput,MouseMove', blocking=False)
print("Bloqueando ")
imagen = subprocess.Popen(['i_view64.exe','FondoV2.png', '/fs'])

cardmonitor = CardMonitor()
cardobserver = ObservaTarjeta()
cardmonitor.addObserver(cardobserver)

loop = asyncio.get_event_loop()
try:
    loop.run_forever()
finally:
    loop.close()