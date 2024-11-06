
import pygame


pygame.mixer.init()

def play_waka(flag):
    if flag:  
        pygame.mixer.music.load("Pacman/music/waka-waka.mp3")
        pygame.mixer.music.play()

        