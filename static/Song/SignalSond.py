import pygame

def emiteSom():
    pygame.mixer.init()
    pygame.mixer.music.load('son.wav')
    pygame.mixer.music.play()

emiteSom()