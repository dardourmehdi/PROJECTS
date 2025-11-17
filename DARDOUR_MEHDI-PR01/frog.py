import pygame
from config import FROG_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH, LANE_HEIGHT, LIVES 

# Charger l'image de la grenouille
frog_img = pygame.image.load("images/frog.png")
frog_img = pygame.transform.scale(frog_img, (FROG_SIZE, FROG_SIZE))

# ======================== PARTIE 1.1 ========================
# TODO : Dans le dictionnaire `frog_dict` suivant : 
# 
# Vous devez remplacer les valeurs des clés "x" et "y", de sorte à ce que
# la grenouille apparaisse au centre de la première voie de pelouse (en bas de l’écran).
# Utilisez les constantes SCREEN_WIDTH, SCREEN_HEIGHT, LANE_HEIGHT et FROG_SIZE pour faire le calcul.

frog_dict = {
    "x": SCREEN_WIDTH / 2 - (FROG_SIZE / 2),
    "y": SCREEN_HEIGHT - LANE_HEIGHT / 2 - (FROG_SIZE / 2),
    "size": FROG_SIZE,
    "speed": LANE_HEIGHT,
    "on_log": False, # Si la grenouille se retrouve sur la bûche (True) ou non (False)
    "log_speed": 0, 
    "in_water": False,
    "water_timer": 0,
    "has_won": False,
    "lives": LIVES
}

# ===============================================================
