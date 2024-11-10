import pygame

pygame.mixer.init()
waka_sound = pygame.mixer.Sound("Pacman/music/waka-waka.mp3")
death_sound = pygame.mixer.Sound("Pacman/music/pacman_death.wav")

pygame.mixer.Sound.set_volume(waka_sound, 0.5)
pygame.mixer.Sound.set_volume(death_sound, 0.5)

def play_waka(flag):
    if flag:
        if not pygame.mixer.get_busy():
            pygame.mixer.Sound.play(waka_sound)
    else:
        pygame.mixer.Sound.stop(waka_sound)

def play_death_sound():
    pygame.mixer.Sound.play(death_sound) 
            