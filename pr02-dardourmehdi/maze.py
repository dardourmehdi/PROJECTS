import pygame
from constants import *
import numpy as np
import random

class Maze:
    """Maze class that handles the game board and collision detection"""
    
    def __init__(self):
        self.width = MAZE_WIDTH
        self.height = MAZE_HEIGHT
        self.cell_width = CELL_WIDTH
        self.cell_height = CELL_HEIGHT

        # Create a simple maze layout (1 = wall, 0 = empty)
        self.layout = np.array([
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,0,1],
            [1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1],
            [1,0,1,1,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,0,1],
            [1,0,1,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,1,0,1],
            [1,0,1,1,1,0,1,0,1,1,0,0,0,0,0,1,1,0,1,0,1,1,1,0,1],
            [1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1],
            [1,0,1,1,1,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,1,1,1,0,1],
            [1,0,1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,0,1],
            [1,0,1,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,1,0,1],
            [1,0,1,1,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,0,1],
            [1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1],
            [1,1,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,0,1,0,1,0,1,1,1],
            [1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1],
            [1,0,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ])

        self.portail_orange_cell, self.portail_bleu_cell = self.positions_portails()

        self.portail_or_img = None
        self.portail_bl_img = None

    def is_wall_collision(self, hitbox):
        """Check if the given rectangle collides with any walls"""
        # TODO: Écrire votre code ici
        centre_x = hitbox.centerx
        centre_y = hitbox.centery
        colonne = int(centre_x // self.cell_width)
        ligne = int(centre_y // self.cell_height)

        grille = [(ligne-1, colonne-1), (ligne-1, colonne), (ligne-1, colonne+1),
                  (ligne, colonne-1), (ligne, colonne), (ligne, colonne+1),
                  (ligne+1, colonne-1), (ligne+1, colonne), (ligne+1, colonne+1)]
        
        for l,c in grille:
            if 0<= l < self.layout.shape[0] and 0<= c < self.layout.shape[1]:
                if self.layout[l][c] == 1 :
                    x = c * self.cell_width
                    y = l * self.cell_height
                    hitbox_mur = pygame.Rect(x,y,self.cell_width, self.cell_height)

                    if hitbox.colliderect(hitbox_mur):
                        return True 
        return False

    def positions_portails(self):
        '''Cette méthode permet de choisir les positions aléatoires des portails aux endroits libre selon le maze'''
        cell_libre = []
        for i in range(self.layout.shape[0]):
            for j in range(self.layout.shape[1]):
                if self.layout[i,j] == 0 :
                    cell_libre.append((i,j))
        
        cell_orange, cell_bleu = random.sample(cell_libre,2)
        return cell_orange, cell_bleu
    
    def rectangles_portails(self):
        """Cette méthode permet de créer des rectangles pygames associés aux portails qui seront utiles plus tard"""
        rect_orange = pygame.Rect(self.portail_orange_cell[1] * self.cell_width,self.portail_orange_cell[0] * self.cell_height, self.cell_width, self.cell_height )
        rect_bleu = pygame.Rect(self.portail_bleu_cell[1] * self.cell_width,self.portail_bleu_cell[0] * self.cell_height, self.cell_width, self.cell_height )
        return rect_orange, rect_bleu
    
    def draw(self, screen):
        """Draw the maze on the screen"""
        
        for row in range(self.height):
            for col in range(self.width):
                if self.layout[row,col] == 1:  # Wall
                    x = col * self.cell_width
                    y = row * self.cell_height
                    wall_rect = pygame.Rect(x, y, self.cell_width, self.cell_height)
                    pygame.draw.rect(screen, BLUE, wall_rect)
                    
                    # Add border for better visibility
                    pygame.draw.rect(screen, WHITE, wall_rect, 1)
        
        rect_orange, rect_bleu = self.rectangles_portails()

        if self.portail_or_img is None : 
            self.portail_or_img = pygame.transform.scale(pygame.image.load("imgs/portail_orange.png"), (self.cell_width, self.cell_height))
        if self.portail_bl_img is None : 
            self.portail_bl_img = pygame.transform.scale(pygame.image.load("imgs/portail_bleu.png"), (self.cell_width, self.cell_height))
        
        screen.blit(self.portail_bl_img, (rect_bleu.x, rect_bleu.y))
        screen.blit(self.portail_or_img, (rect_orange.x, rect_orange.y))

    
    def get_valid_positions(self):
        """Get all valid (non-wall) positions for placing objects"""
        valid_positions = []
        
        for row in range(self.height):
            for col in range(self.width):
                if self.layout[row,col] == 0:  # Empty space
                    x = col * self.cell_width + self.cell_width // 2
                    y = row * self.cell_height + self.cell_height // 2
                    valid_positions.append((x, y))

        return valid_positions