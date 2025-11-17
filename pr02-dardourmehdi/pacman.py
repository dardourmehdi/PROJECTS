import pygame
import math
from game_object import GameObject
from constants import *

class Pacman(GameObject):
    """Pacman player class"""
    
    def __init__(self, x, y):
        super().__init__(x, y, CELL_WIDTH//1.8, CELL_HEIGHT//1.8, YELLOW)
        self.start_x = x
        self.start_y = y
        self.direction = 0  # 0=right, 1=down, 2=left, 3=up
        self.next_direction = 0
        self.speed = PACMAN_SPEED
        self.mouth_open = True
        self.mouth_timer = 0
        self.x = x - self.width // 2
        self.y = y - self.height // 2
        self.dans_portail = None       #nous permet d'éviter les ping-pong !
    
    def téléportation(self,maze):
        rect_pacman = pygame.Rect(self.x, self.y, self.width, self.height)
        rect_orange, rect_bleu = maze.rectangles_portails()

        dans_portail_or = rect_pacman.colliderect(rect_orange)
        dans_portail_bl = rect_pacman.colliderect(rect_bleu)

        if not dans_portail_bl and not dans_portail_or:
            self.dans_portail = None
            return 
        
        if dans_portail_bl and self.dans_portail != 'dans_bleu':
            self.x = rect_orange.x + (rect_orange.width - rect_orange.height ) // 2
            self.y = rect_orange.y + (rect_orange.width - rect_orange.height ) // 2
            self.dans_portail = 'dans_orange'
        
        if dans_portail_or and self.dans_portail != 'dans_orange':
            self.x = rect_bleu.x + (rect_bleu.width - rect_bleu.height ) // 2
            self.y = rect_bleu.y + (rect_bleu.width - rect_bleu.height ) // 2
            self.dans_portail = 'dans_bleu'


    def handle_input(self, key):
        """Handle keyboard input for movement"""
        # TODO: Écrire votre code ici
        if key == pygame.K_RIGHT:
            self.next_direction = 0 
        elif key == pygame.K_LEFT:
            self.next_direction = 2
        elif key == pygame.K_DOWN:
            self.next_direction = 1
        elif key == pygame.K_UP:
            self.next_direction = 3
        


    def update(self, maze):
        """Update Pacman's position and state"""
        # Update mouth animation
        self.mouth_timer += 1
        if self.mouth_timer >= 10:
            self.mouth_open = not self.mouth_open
            self.mouth_timer = 0
        
        # Get next position based on next_direction
        new_x, new_y, hitbox = self.get_next_position()

        # Check if there is collision with a wall
        if not maze.is_wall_collision(hitbox):
            self.direction = self.next_direction
            self.x = new_x
            self.y = new_y
        
        self.téléportation(maze)

    def get_next_position(self):
        """
        Get the next position based on direction

        The hitbox will be used to detect collisions before moving.
        Returns new_x, new_y, hitbox
        """
        new_x, new_y = self.x, self.y
        hitbox = None
        # TODO: Écrire votre code ici
        if self.next_direction == 0 : 
            new_x += self.speed 
        elif self.next_direction == 1 :
            new_y += self.speed
        elif self.next_direction == 2 :
            new_x -= self.speed 
        elif self.next_direction == 3 : 
            new_y -= self.speed
        hitbox = pygame.Rect(new_x,new_y,self.width, self.height)
        return new_x, new_y, hitbox

    
    def draw(self, screen):
        """Draw Pacman with mouth animation"""
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        radius = self.width // 2

        # TODO: Écrire votre code ici
        # Draw Pacman body
        if not self.mouth_open :
            pygame.draw.circle(screen, YELLOW, (center_x,center_y), radius)
        else:
            if self.direction == 0 : 
                angle = 0
            elif self.direction == 1 : 
                angle = math.pi / 2
            elif self.direction == 2 : 
                angle = math.pi
            else:
                angle = -math.pi/2
            
            angle_arc_haut = angle - math.pi / 6
            angle_arc_bas = angle + math.pi / 6
            pas = math.radians(5)
            ang = angle_arc_bas
            liste_points = [(center_x, center_y)]
            while ang <= (angle_arc_haut + 2*math.pi) : 
                x = center_x + math.cos(ang) * radius
                y = center_y + math.sin(ang) * radius
                liste_points.append((x,y))
                ang += pas
            liste_points.append((center_x, center_y))

            pygame.draw.polygon(screen, YELLOW, liste_points, 0)

        # Draw Pacman eye

        if self.direction == 0 : 
            pygame.draw.circle(screen , BLACK, (self.x + self.width // 2, self.y + self.width // 2 - 5 ), 2.0)
        elif self.direction == 1 :
            pygame.draw.circle(screen , BLACK, (self.x + self.width // 2 + 5, self.y + self.width // 2 ),2.0)
        elif self.direction == 2 :
            pygame.draw.circle(screen , BLACK, (self.x + self.width // 2, self.y + self.width // 2 - 5 ),2.0)
        else:
            pygame.draw.circle(screen , BLACK, (self.x + self.width // 2 - 5, self.y + self.width // 2 ),2.0)


    
    def reset_position(self):
        """Reset Pacman to starting position"""
        self.x = self.start_x - self.width // 2
        self.y = self.start_y - self.height // 2
        self.direction = 0
        self.next_direction = 0