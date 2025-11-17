from config import LANES, SCREEN_HEIGHT, SCREEN_WIDTH, FROG_SIZE, LIVES 
from window import GAME_WINDOW
from frog import frog_dict
import pygame
import sys

# Fonction qui gère le mouvement des entités (voitures et bûches de bois)
def move_entities():
    for lane in LANES:
        for ent in lane["entities"]:
            ent["x"] += lane["speed"]
            if lane["speed"] > 0 and ent["x"] > SCREEN_WIDTH:
                ent["x"] = -200
            elif lane["speed"] < 0 and ent["x"] < -200:
                ent["x"] = SCREEN_WIDTH + 100

# ======================== PARTIE 1.2 ==========================
# TODO : Complétez la fonction `handle_input()` pour mettre à jour la position de la grenouille
# lorsqu'on appuie sur une flèche du clavier. 
#
# TODO : Ajoutez une contrainte pour empêcher la grenouille de sortir de l'écran.
# Les coordonnées "x" et "y" doivent rester entre les bornes de la fenêtre de jeu.

def handle_input(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            frog_dict["x"] = max(0, frog_dict["x"] - frog_dict["speed"])
        
        if event.key == pygame.K_RIGHT:
            frog_dict["x"] = min(SCREEN_WIDTH - FROG_SIZE, frog_dict["x"] + frog_dict["speed"])

        if event.key == pygame.K_UP:
            frog_dict["y"] = max(0, frog_dict["y"] - frog_dict["speed"])

        if event.key == pygame.K_DOWN:
            frog_dict["y"] = min( SCREEN_HEIGHT - FROG_SIZE, frog_dict["y"] + frog_dict["speed"])
    
# ===============================================================



# ======================== PARTIE 2.3 ===========================
#
# TODO : Complétez la fonction `check_collision`, qui détecte les collisions entre la grenouille
# et les voitures. 
# 
# Étapes à suivre : 
# - Créer un rectangle (`pygame.Rect`) représentant la grenouille. 
# - Parcourir toutes les voies de type "car" dans la liste "lanes".
# - Pour chaque voiture dans une voie : 
#     - Créer un rectangle basé sur l'image et la position de la voiture
#     - Vérifier si ce rectangle entre en collision avec celui de la grenouille, à l'aide
#       de la méthode .colliderect(). 
# - Retourner "True" si une collision est détectée, sinon "False". 
# 
# Voir le README.md pour des détails supplémentaires sur les fonctions pygame. 

def check_collision():
    frog = pygame.Rect(frog_dict["x"], frog_dict["y"], FROG_SIZE, FROG_SIZE)
    for voie in LANES:
        if voie["type"] == "road" :
            for car in voie["entities"]:
                voiture = pygame.Rect(car["x"], car["y"], car["width"], car["height"] )
                if frog.colliderect(voiture):
                    return True

    return False

# =================================================================


# ======================== PARTIE 3.3 =============================
#
# TODO : Complétez la fonction 'handle_logs()', qui gère la logique de détection pour savoir
# si la grenouille se retrouve sur une bûche dans la rivière. 
# 
# Étapes à suivre :
# - Réinitialiser frog["on_log"] à False
# - Créer un rectangle (pygame.Rect) autour de la grenouille, en ajoutant une marge pour que la détection soit plus précise.
# - Parcourir les quatre voies de type "log" dans lanes.
# - Pour chaque bûche, créez un rectangle de collision basé sur sa position et largeur.
# - Si une collision est détectée entre la grenouille et une bûche :
# - Mettez frog["on_log"] à True.
# - Assignez la vitesse de la bûche à frog["log_speed"].
# - Sortez de la fonction (return).
# - Si aucune bûche n'est en contact avec la grenouille, la variable frog["log_speed"] doit être remise à 0.

def handle_logs():
    frog = pygame.Rect(frog_dict["x"], frog_dict["y"], FROG_SIZE, FROG_SIZE)
    frog_dict["on_log"] = False
    frog_dict["log_speed"] = 0
    for voie in LANES:
        if voie["type"] == "river" :
            for log in voie["entities"]:
                buche = pygame.Rect(log["x"], log["y"], log["width"], log["height"] )
                if frog.colliderect(buche):
                    frog_dict["on_log"] = True 
                    frog_dict["log_speed"] = voie["speed"]
                    return

# =================================================================

# Vérifier si le joueur a gagné (si la grenouille a atteint la dernière voie de pelouse)
def check_win():
    for lane in LANES:
        if lane["type"] == "grass_win":
            if abs(lane["y"] - frog_dict["y"]) < 12:
                return True
    return False

# Réinitialisation de la position de la grenouille 
def reset_frog(decrease_life=True):
    if decrease_life:
        frog_dict["lives"] -= 1
    frog_dict["x"] = SCREEN_WIDTH // 2 - FROG_SIZE // 2
    frog_dict["y"] = SCREEN_HEIGHT - FROG_SIZE - 10
    frog_dict["in_water"] = False
    frog_dict["water_timer"] = 0
    frog_dict["on_log"] = False
    frog_dict["log_speed"] = 0
    frog_dict["has_won"] = False

# Fonction qui permet d'attendre que l'utilisateur appuie sur la touche "Entrée" (pour redémarrer le jeu)
def wait_for_enter():
    font_small = pygame.font.SysFont(None, 36)
    prompt_text = font_small.render("Press ENTER to play again", True, (255, 255, 255))
    prompt_rect = prompt_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    waiting = False
                    reset_frog(decrease_life=False)  # réinitialiser la position de la grenouille
                    frog_dict["lives"] = LIVES # réinitialiser le nombre de vies à LIVES

        # Dessine le message à chaque "frame"
        GAME_WINDOW.blit(prompt_text, prompt_rect)
        pygame.display.update()
