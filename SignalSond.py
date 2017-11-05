import pygame

def emiteSomOk():
    pygame.mixer.init()
    pygame.mixer.music.load('son.wav')
    pygame.mixer.music.play()

def emiteSomErro():
    pygame.mixer.init()
    pygame.mixer.music.load('erro.wav')
    pygame.mixer.music.play()

def emiteSomLogin():
    pygame.mixer.init()
    pygame.mixer.music.load('login.wav')
    pygame.mixer.music.play()