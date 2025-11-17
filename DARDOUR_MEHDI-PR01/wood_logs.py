import pygame
from config import LOG_SIZES

# ======================== PARTIE 3.1 ===========================
# 
# TODO : Définir un dictionnaire pour les bûches en bois avec trois tailles différentes : petite, moyenne et longue
# 
# Étapes à suivre : 
# - Créer un dictionnaire nommé `logs_dict` avec les trois clés suivantes : 
#      - short
#      - medium
#      - long 
#
# - Utilisez "pygame.image.load()" pour charger l'image "log.png" (à partir du dossier "images/")
#   trois fois, c'est-à-dire une fois pour chaque taille.
# - Redimensionnez (avec "pygame.transform.scale") chaque image en utilisant les clés du dictionnaire LOG_SIZES. 

logs_dict = {"short" : pygame.transform.scale( pygame.image.load("images/log.png") , LOG_SIZES["short"] )
            ,"medium" : pygame.transform.scale( pygame.image.load("images/log.png") , LOG_SIZES["medium"]) 
            ,"long" : pygame.transform.scale( pygame.image.load("images/log.png") , LOG_SIZES["long"]) }


# ===============================================================