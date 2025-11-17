import pygame
import sys
from config import FPS, LANE_HEIGHT, LANES, LIVES
from window import add_road_lanes, add_grass_lane, add_river_lanes, add_final_grass_lane, draw_window, show_win_message, show_game_over_message
from game import move_entities, handle_input, check_collision, handle_logs, check_win, reset_frog, wait_for_enter
from frog import frog_dict

# Initialiser Pygame
pygame.init()

# Appele les fonctions pour ajouter les voies et leurs entités (voitures et bûches)
add_road_lanes()
add_grass_lane()
add_river_lanes()
add_final_grass_lane()

# Boucle principale du jeu
def main():
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            handle_input(event)

        # Appelle la fonction pour déplacer les entités 
        move_entities()

        # Appelle la fonction qui gère la logique pour les bûches de bois 
        handle_logs()

        # Si la grenouille est sur une bûche, elle suit son mouvement
        if frog_dict["on_log"]:
            frog_dict["x"] += frog_dict["log_speed"]

        current_time = pygame.time.get_ticks()

        # Vérifier si on est dans une voie de log (rivière)
        in_log_lane = any(
            lane["type"] == "river" and
            frog_dict["y"] + frog_dict["size"] > lane["y"] and  # bas grenouille > haut voie
            frog_dict["y"] < lane["y"] + LANE_HEIGHT    # haut grenouille < bas voie
            for lane in LANES
        )

        # Si dans rivière, pas sur bûche, et pas déjà en état eau
        if in_log_lane and not frog_dict["on_log"] and not frog_dict["in_water"]:
            frog_dict["in_water"] = True
            frog_dict["water_timer"] = current_time

        # Si dans l’eau, attend 300 ms avant d'appeler reset_frog
        if frog_dict["in_water"]:
            if current_time - frog_dict["water_timer"] >= 300:
                print("Frogger est tombée à l'eau : –1 vie!")
                reset_frog(decrease_life=True)

        if check_collision():
            print("Collision avec une voiture : –1 vie!")
            reset_frog(decrease_life=True)

        # Si on a gagné
        if check_win() and not frog_dict.get("has_won", False):
            frog_dict["has_won"] = True
            draw_window()
            pygame.display.update()
            show_win_message()
            wait_for_enter()
            frog_dict["lives"] = LIVES
            reset_frog(decrease_life=False)

        if frog_dict["lives"] <= 0:
            show_game_over_message()
            wait_for_enter()
            frog_dict["lives"] = LIVES
            reset_frog(decrease_life=False)

        draw_window()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
