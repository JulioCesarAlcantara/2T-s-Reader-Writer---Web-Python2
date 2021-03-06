# -*- coding: utf8 -*-

 GPIO
import signal

import MFRC522


class writerTag():

    def __init__(self, codThings):
        continue_reading = True
        self.texto = codThings
        self.end_read()
        self.methodWriter()


    # Capture SIGINT for cleanup when the script is aborted
    def end_read(signal,frame):
        global continue_reading
        # print ("Ctrl+C captured, ending read.")
        continue_reading = False
        GPIO.cleanup()

    # Hook the SIGINT
    signal.signal(signal.SIGINT, end_read)

    # Create an object of the class MFRC522
    MIFAREReader = MFRC522.MFRC522()

    # This loop keeps checking for chips. If one is near it will get the UID and authenticate
    def methodWriter(self, code):
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
                print ("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))

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

                    # texto = "88670"
                    # print("------texto------")
                    # print(len(texto))


                        data1 = []
                       # data2 = []

                        for x in range(0, 16-int(len(self.texto))):
                            data1.append(0x00)


                        for digito in code:
                            data1.append(int(digito))

                        # print ("Sector 8 looked like this:")
                        # Read block 8
                        MIFAREReader.MFRC522_Read(bloco1)
                          #  MIFAREReader.MFRC522_Read(bloco2)
                          #   print ("\n")

                            # print ("Sector 8 will now be filled with 0xFF:")
                            # Write the data
                        MIFAREReader.MFRC522_Write(bloco1, data1)
                           # MIFAREReader.MFRC522_Write(bloco2, data2)
                           #  print ("\n")

                            # print ("It now looks like this:")
                            # Check to see if it was written
                        MIFAREReader.MFRC522_Read(bloco1)
                            #MIFAREReader.MFRC522_Read(bloco2)
                            # print ("\n")

                        data = []
                            # Fill the data with 0x00
                        for x in range(0,16):
                             data.append(0x00)

                            # print ("Now we fill it with 0x00:")
                        MIFAREReader.MFRC522_Write(bloco1, data1)
                            #MIFAREReader.MFRC522_Write(bloco2, data2)
                            # print ("\n")

                            # print ("It is now empty:")
                            # Check to see if it was written
                        MIFAREReader.MFRC522_Read(bloco1)
                            #MIFAREReader.MFRC522_Read(bloco2)
                            # print ("\n")


                            # Stop
                        MIFAREReader.MFRC522_StopCrypto1()

                            # Make sure to stop reading for cards
                        continue_reading = False
                else:
                    print ("Authentication error")