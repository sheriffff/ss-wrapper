import pygame
import time


def play_clip(clip_path, times=10):
    pygame.mixer.init()
    pygame.mixer.music.load(clip_path)

    for _ in range(times):
        time.sleep(1)
        pygame.mixer.music.play()
