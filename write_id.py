#!/usr/bin/env python3
# -*- coding: utf8 -*-

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

def start(string):
    texto = string
    # things = Things ()
    # location = things.search_locations ()
    #
    # dados = []
    # dados.append(things.search_things_by_num1(texto))

    #
    # render_template ('/writer.html', tagAtiv="Tag Activated Successfully !!")

    continue_reading = True
    # Hook the SIGINT
    # signal.signal(signal.SIGINT, end_read)
    is_main_thread()
    # Create an object of the class MFRC522
    MIFAREReader = MFRC522.MFRC522()

    # This loop keeps checking for chips. If one is near it will get the UID and authenticate
    while continue_reading:

        # Scan for cards
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        # If a card is found
        if status == MIFAREReader.MI_OK:
            print ("Card detected")

        # Get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_Anticoll()

        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:

            # Print UID
            # print ("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))

            # This is the default key for authentication
            key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]

            # Select the scanned tag
            MIFAREReader.MFRC522_SelectTag(uid)

            # Authenticate
            bloco1 = 1
        #bloco2 = 2

            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, bloco1, key, uid)
            print ("\n")

            # Check if authenticated
            if status == MIFAREReader.MI_OK:

                # Variable for the data to write

            #print("------texto------")
            #print(len(texto))


                data1 = []

                for x in range(0, 16-int(len(texto))):
                    data1.append(0x00)


                for digito in texto:
                    data1.append(int(digito))

                # print ("Sector 8 looked like this:")
                # Read block 8
                MIFAREReader.MFRC522_Read(bloco1)
                print ("\n")



                # print ("Sector 8 will now be filled with 0xFF:")
                # Write the data
                write = MIFAREReader.MFRC522_Write(bloco1, data1)
                print ("\n")
                if write == True:
                    return True
                    # MIFAREReader.MFRC522_StopCrypto1 ()
                    # render_template ('/writer.html', msg="Tag Activated Successfully !!", locations=location)
                else:
                    return False
                    # MIFAREReader.MFRC522_StopCrypto1 ()
                    # render_template ('/writer.html', erro="Tag Activation Error !!", locations=location)

                # print ("It now looks like this:")
                # Check to see if it was written
                # MIFAREReader.MFRC522_Read(bloco1)
                # print ("\n")


                # data = []
                # Fill the data with 0x00
                #for x in range(0,16):
                 #   data.append(0x00)

                # print ("Now we fill it with 0x00:")
                # MIFAREReader.MFRC522_Write(bloco1, data1)
                # print ("\n")

                # print ("It is now empty:")
                # Check to see if it was written
                # MIFAREReader.MFRC522_Read(bloco1)
                # print ("\n")

                # Stop
                MIFAREReader.MFRC522_StopCrypto1()

                # Make sure to stop reading for cards
                continue_reading = False
            else:
                print ("Authentication error")



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