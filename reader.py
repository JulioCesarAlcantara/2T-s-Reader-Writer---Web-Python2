#!/usr/bin/env python3
# -*- coding: utf8 -*-
import json

import RPi.GPIO as GPIO
from flask import render_template

import MFRC522
import signal



# Capture SIGINT for cleanup when the script is aborted
from Things import Things


def end_read(signal,frame):

    global continue_reading
    print ("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()

def startLeitura():
    continue_reading = True
    print "Aqui 1"
    # Hook the SIGINT
    # signal.signal(signal.SIGINT, end_read)
    is_main_thread()
    # Create an object of the class MFRC522
    MIFAREReader = MFRC522.MFRC522()
    array = []
    # This loop keeps checking for chips. If one is near it will get the UID and authenticate
    while continue_reading:
        print "Aqui 2"
        (status, TagType) = MIFAREReader.MFRC522_Request (MIFAREReader.PICC_REQIDL)

        # If a card is found
        if status == MIFAREReader.MI_OK:
            print "Card detected"

        # Get the UID of the card
        (status, uid) = MIFAREReader.MFRC522_Anticoll ()

        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:

            # Print UID
            print "Card read UID: " + str (uid[0]) + "," + str (uid[1]) + "," + str (uid[2]) + "," + str (uid[3])

            # This is the default key for authentication
            key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

            # Select the scanned tag
            MIFAREReader.MFRC522_SelectTag (uid)
            print "Aqui 3"
            # Sector
            sectorBlock = 1
            # sectorBlock2 = 2

            # Authenticate
            status = MIFAREReader.MFRC522_Auth (MIFAREReader.PICC_AUTHENT1A, sectorBlock, key, uid)
            print("-----------")
            print (uid)
            print "Aqui 4"

            # Check if authenticated
            if status == MIFAREReader.MI_OK:
                print "Aqui 5"
                numero = MIFAREReader.MFRC522_Read (sectorBlock)
                print "Aqui 6"

                things = Things()
                print "Aqui 7"

                array.append(things.search_things_by_num2 (numero))
                print "Aqui 8"
                MIFAREReader.MFRC522_StopCrypto1 ()
                # thingsRead = json.dumps(para_dict(array))
                print "Aqui 9"


                # try:
                #     arquivo = open ('listRead.json', "w")
                #     arquivo.write(thingsRead)
                #     arquivo.close()
                #     print "SUCESSO"
                #     return array
                # except Exception as e:
                #     print "ERRO AQUI !!!"
                #     return False
            else:
                print "Não achou nada !!"
                return 0
        print "Aqui 10"
        return array

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