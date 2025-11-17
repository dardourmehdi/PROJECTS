import pygame
import random
from game_object import GameObject
from constants import *

class Ghost(GameObject):
    """Base Ghost class"""
    
    def __init__(self, x, y, color):
        super().__init__(x, y, int(CELL_WIDTH//2), int(CELL_HEIGHT//1.2), color)
        self.start_x = x
        self.start_y = y
        self.direction = random.randint(0, 3)
        self.speed = GHOST_SPEED
        self.vulnerable = False
        self.vulnerable_timer = 0
        self.vulnerable_duration = 300  # frames
        self.step = "left"
        self.step_timer = 0
        self.last_RL_direction = 0
        self.x = x - self.width // 2
        self.y = y - self.height // 2
        self.dans_portail = None

    def update(self, maze, pacman):
        """Update ghost position and state"""
        # Update vulnerable state
        if self.vulnerable:
            self.vulnerable_timer += 1
            if self.vulnerable_timer >= self.vulnerable_duration:
                self.vulnerable = False
                self.vulnerable_timer = 0
        
        # Update ghost animation
        self.step_timer += 1
        if self.step_timer >= 10:
            self.step = "right" if self.step == "left" else "left"
            self.step_timer = 0
        
        # Move ghost
        self.move(maze, pacman)
    
    def move(self, maze, pacman):
        """Basic ghost movement (random direction on collision)"""
        new_x, new_y, hitbox = self.get_next_position()
        
        # Check for collision with walls
        if maze.is_wall_collision(hitbox):
            # Change direction randomly
            self.direction = random.randint(0, 3)
        else:
            self.x = new_x
            self.y = new_y
        
        self.téléportation(maze)
    
    def téléportation(self,maze):
        rect_ghost = pygame.Rect(self.x, self.y, self.width, self.height)
        rect_orange, rect_bleu = maze.rectangles_portails()

        dans_portail_or = rect_ghost.colliderect(rect_orange)
        dans_portail_bl = rect_ghost.colliderect(rect_bleu)

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

    
    def get_next_position(self):
        """Get next position based on current direction"""
        new_x, new_y = self.x, self.y
        hitbox = None

        if self.direction in [0, 2]:  # Right or Left
            self.last_RL_direction = self.direction
        
        # TODO: Écrire votre code ici

        if self.direction == 0 : 
            new_x += self.speed
        elif self.direction == 1 :
            new_y += self.speed 
        elif self.direction == 2 : 
            new_x -= self.speed 
        else:
            new_y -= self.speed
        
        hitbox = pygame.Rect(new_x, new_y, self.width, self.height)

        
        return new_x, new_y, hitbox
            
    def draw(self, screen):
        """Load ghost image"""
        if self.vulnerable == False:
            ghost = pygame.image.load(f"imgs/{self.color}_ghost.png")
        else:
            ghost = pygame.image.load(f"imgs/weak_ghost.png")
        
        ghost = pygame.transform.scale(ghost, (self.width, self.height))

        if self.last_RL_direction == 0 : 
            ghost = pygame.transform.flip(ghost, True, False)
        if self.step == "right":
            rotation = pygame.transform.rotate(ghost,10)
        else:
            rotation = pygame.transform.rotate(ghost,-10)
        screen.blit(rotation, (self.x, self.y))
    
    def make_vulnerable(self):
        """Make the ghost vulnerable to being eaten"""
        self.vulnerable = True
        self.vulnerable_timer = 0
    
    def reset_position(self):
        """Reset ghost to starting position"""
        self.x = self.start_x - self.width // 2
        self.y = self.start_y - self.height // 2
        self.vulnerable = False
        self.vulnerable_timer = 0

class RedGhost(Ghost):
    """Red ghost - aggressive, chases Pacman directly"""
    
    def __init__(self, x, y, color="red"):
        super().__init__(x, y, color)

    def move(self, maze, pacman):
        """Aggressive movement - chase Pacman directly"""
        if self.vulnerable:
            # Run away from Pacman when vulnerable
            self.flee_from_pacman(maze, pacman)
        else:
            # Chase Pacman
            self.chase_pacman(maze, pacman)
    
    def chase_pacman(self, maze, pacman):
        """Move towards Pacman"""
        pacman_x, pacman_y = pacman.get_position()
        ancienne_direction = self.direction
        # TODO: Écrire votre code ici

        if abs(pacman_x - self.x) >= abs(pacman_y - self.y) :
            if pacman_x > self.x :
                self.direction = 0
            else:
                self.direction = 2    
        else:
            if pacman_y > self.y:
                self.direction = 1
            else:
                self.direction = 3
        nv_x, nv_y, hitbox = self.get_next_position()
        if maze.is_wall_collision(hitbox):
            self.direction = ancienne_direction
            super().move(maze, pacman)
        else:
            self.x = nv_x
            self.y = nv_y

    def flee_from_pacman(self, maze, pacman):
        """Run away from Pacman when vulnerable"""
        pacman_x, pacman_y = pacman.get_position()

        # TODO: Écrire votre code ici

        meilleur_dist = max(abs(self.x - pacman_x), abs(self.y - pacman_y))
        meilleur_dir = self.direction

        for direction in range(0,4):
            self.direction = direction
            new_x, new_y, hitbox = self.get_next_position()
            if maze.is_wall_collision(hitbox):
                continue
            distance_courante = max(abs(new_x - pacman_x), abs(new_y - pacman_y))

            if distance_courante > meilleur_dist : 
                meilleur_dist = distance_courante
                meilleur_dir = direction
        
        self.direction = meilleur_dir
        super().move(maze, pacman)
                

class PinkGhost(Ghost):
    """Pink ghost - tries to ambush Pacman"""

    def __init__(self, x, y, color="pink"):
        super().__init__(x, y, color)

    def move(self, maze, pacman):
        """Ambush movement - try to get ahead of Pacman"""
        if self.vulnerable:
            super().move(maze, pacman)  # Random movement when vulnerable
        else:
            self.ambush_pacman(maze, pacman)

    def ambush_pacman(self, maze, pacman):
        """Try to position ahead of Pacman"""
        # Try to position ahead of Pacman

        # TODO: Écrire votre code ici
        pacman_x, pacman_y = pacman.get_position()
        ancienne_direction = self.direction

        cible_x = pacman_x + (pacman_x - self.x)/2
        cible_y = pacman_y + (pacman_y - self.y)/2

        if abs(cible_x - self.x) >= abs(cible_y - self.y):
            if cible_x - self.x > 0 :
                self.direction = 0
                self.last_RL_direction = 0
            else :
                self.direction = 2
                self.last_RL_direction = 2
        
        else:
            if cible_y - self.y > 0 :
                self.direction = 1
            else:
                self.direction = 3
        
        nv_x, nv_y,hitbox = self.get_next_position()
        if maze.is_wall_collision(hitbox):
            self.direction = ancienne_direction
            super().move(maze, pacman)
        else:
            self.x = nv_x
            self.y = nv_y

        

class BlueGhost(Ghost):
    """Blue ghost - patrol behavior"""

    def __init__(self, x, y, color="blue"):
        super().__init__(x, y, color)
        self.patrol_timer = 0
        self.patrol_duration = 120
    
    def move(self, maze, pacman):
        """Patrol movement - changes direction periodically"""
        # TODO: Écrire votre code ici
        self.patrol_timer += 1
        hitbox = self.get_next_position()[2]
        if maze.is_wall_collision(hitbox) :
            self.direction = random.randint(0, 3)
        
        elif self.patrol_timer >= self.patrol_duration:
            self.direction = random.randint(0, 3)
            self.patrol_timer = 0

        super().move(maze, pacman)

class OrangeGhost(RedGhost):
    """Orange ghost - mixed behavior"""

    def __init__(self, x, y, color="orange"):
        super().__init__(x, y, color)
        self.behavior_timer = 0
        self.chase_mode = True
        self.behavior_duration = 180  # frames
    
    def move(self, maze, pacman):
        """Mixed behavior - alternates between chasing and fleeing"""
        self.behavior_timer += 1
        
        # TODO: Écrire votre code ici

        if self.vulnerable : 
            self.flee_from_pacman(maze, pacman)
            return

        if self.chase_mode :
            self.chase_pacman(maze, pacman)
        else:
            hitbox = self.get_next_position()[2]
            if maze.is_wall_collision(hitbox):
                self.direction = random.randint(0,3)
            super().move(maze, pacman)

        if self.behavior_timer >= self.behavior_duration:
            self.chase_mode =  not self.chase_mode
            self.behavior_timer = 0



ghosts_dict = {
            "red": RedGhost,
            "pink": PinkGhost,
            "blue": BlueGhost,
            "orange": OrangeGhost
        }