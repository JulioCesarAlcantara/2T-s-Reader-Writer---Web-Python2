#!/usr/bin/env python3
# -*- coding: utf8 -*-
import json

import RPi.GPIO as GPIO
from flask import render_template

import MFRC522
import signal
from SignalSond import *



# Capture SIGINT for cleanup when the script is aborted
from Things import Things

def end_read(signal,frame):

    global continue_reading
    print ("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()

def startLeitura():
    continue_reading = True
    # Hook the SIGINT
    # signal.signal(signal.SIGINT, end_read)

    is_main_thread()
    # Create an object of the class MFRC522
    MIFAREReader = MFRC522.MFRC522()
    array = []
    # This loop keeps checking for chips. If one is near it will get the UID and authenticate
    while continue_reading:
        print "ok 1"
        (status, TagType) = MIFAREReader.MFRC522_Request (MIFAREReader.PICC_REQIDL)
        print "ok 2"
        # If a card is found
        if status == MIFAREReader.MI_OK:
            print "ok 3"
            print "Card detected"

        # Get the UID of the card
            (status, uid) = MIFAREReader.MFRC522_Anticoll ()
            print "ok 4"
        # If we have the UID, continue
        # if status == MIFAREReader.MI_OK:
            print "ok 5"
            # Print UID
            # print "Card read UID: " + str (uid[0]) + "," + str (uid[1]) + "," + str (uid[2]) + "," + str (uid[3])

            # This is the default key for authentication
            key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

            # Select the scanned tag
            MIFAREReader.MFRC522_SelectTag (uid)
            print "ok 6"
            # Sector
            sectorBlock = 1
            # sectorBlock2 = 2

            # Authenticate
            status = MIFAREReader.MFRC522_Auth (MIFAREReader.PICC_AUTHENT1A, sectorBlock, key, uid)

            print("ok 7")

            # Check if authenticated
            # if status == MIFAREReader.MI_OK:
            numero = MIFAREReader.MFRC522_Read (sectorBlock)
            print "ok 8"

            print "NUMERO"
            print numero



            things = Things()

            # return False
            # for i in array:
            # if numero not in i.nr_things1 :
            # array.append(things.search_things_by_num2 (numero))
            emiteSomOk ()
                # else:
                #     emiteSomErro()
                    # yield "Tag already read !!"
            MIFAREReader.MFRC522_StopCrypto1 ()

            return things.search_things_by_num2 (numero)



def is_main_thread():
    try:
        # Backup the current signal handler
        back_up = signal.signal(signal.SIGINT, end_read)
    except ValueError:
        # Only Main Thread can handle signals
        return False
    # Restore signal handler
    signal.signal(signal.SIGINT, end_read)
    return True

def para_dict(obj):
    # Se for um objeto, transforma num dict
    if hasattr(obj, '__dict__'):
        obj = obj.__dict__

    # Se for um dict, le chaves e valores; converte valores
    if isinstance(obj, dict):
        return {k: para_dict(v) for k, v in obj.items()}

    elif isinstance(obj, list) or isinstance(obj, tuple):
        return [para_dict(e) for e in obj]
    else:
        return obj