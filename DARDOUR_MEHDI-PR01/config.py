# Largeur et hauteur de l'écran de jeu 
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 770

# Nombre de voies (incluant les voies de pelouse, route et rivière)
NUM_OF_LANES = 11

# Hauteur des voies
LANE_HEIGHT = SCREEN_HEIGHT // NUM_OF_LANES

# Taille de la grenouille 
FROG_SIZE = 50

# Liste des voies, qui va contenir un dictionnaire contenant les informations suivantes pour chaque voie : 
# "type": soit "road", "river", "grass", ou "grass_win"
    # "speed": la vitesse des entités (ex: voitures ou bûches) dans la voie
    # "y": la position en y de la voie
    # "entities": une liste qui stocke un dictionnaire pour chaque entité (voiture ou bûche) dans la voie
LANES = []

# Liste de couleurs pour les voitures
CAR_COLORS = ["red", "blue", "green", "yellow", "orange", "pink"]

# Taille des voitures
CARS_SIZE = (100, 50)

# Tailles pour les bûches de bois
LOG_SIZES = {
    "short": (60, 40),
    "medium": (80, 40),
    "long": (120, 40)
}

# Nombre de vies initiales de la grenouille
LIVES = 3

# Nombre de "frames per second"
FPS = 60
