# FICHIER CONTENANT LES TRACES DE RECHERCHES DE LA PARTIE 4 DU PROJET 2 - PAR MEHDI DARDOUR 2363106

# CHOIX DES IMAGES
Il fallait, dans la partie 4, utiliser soit des dessins pygame ou bien de images pour représenter les portails. Nous avons alors choisis de rechercher des images de portails et avons sélectionner deux images de portails, un bleu et un orange.

--> Nous les avons nommés portail_bleu.png et portail_orange.png que vous trouverez dans le dossier imgs (créé de base par les concepteurs du projet 2)

# LES MODIFICATIONS DANS maze.py AFIN DE POSITIONNER ALÉATOIREMENT LES PORTAILS 
Premièrement, nous avons ajouté des attributs à la classe maze : self.portail_or_img = None et self.portail_bl_img = None. Entre autre, ces attriburts servent à stocker les images des portails.
Vous remarquerez que nous avons choisis de les initialiser à None, pourquoi ? Et bien c'est pour pouvoir les repoisitionner plus tard sans devoir relancer le programme ! 

De plus, nous avons aussi ajouter les attributs self.portail_orange_cell et self.portail_bleu_cell qui servent à stocker la position des portails.

Passons à présent au méthode que nous avons implémenter dans cette classe : 

### positions_portails(self)
Cette méthode permet en autre de choisir deux positions aléatoires dans la grille où on retrouve des 0, soit des positions libres afin de placer les portails

### rectangles_portails(self)
Cette méthode permet d'associer des rectangles pygame.Rect aux portails selon leurs coordonnées afin de faciliter par la suite leurs implémentation ainsi que les collisions.

### modification de la méthode draw(self)
Nous avons pris la liberté de modifier cette méthode en incorporant :
        
        rect_orange, rect_bleu = self.rectangles_portails()

        if self.portail_or_img is None : 
            self.portail_or_img = pygame.transform.scale(pygame.image.load("imgs/portail_orange.png"), (self.cell_width, self.cell_height))
        if self.portail_bl_img is None : 
            self.portail_bl_img = pygame.transform.scale(pygame.image.load("imgs/portail_bleu.png"), (self.cell_width, self.cell_height))
        
        screen.blit(self.portail_bl_img, (rect_bleu.x, rect_bleu.y))
        screen.blit(self.portail_or_img, (rect_orange.x, rect_orange.y))

Ces lignes de code permettent de charger conditionnelement les images des portails avec la fonction pygame.image.load, puis on choisis de miue les calibrer pour amélorier l'affichage avec pygame.transform.scale selon les dimensions d'une cellule. Enfin, la fonction screen.blit permet d'afficher les portails dans le jeu Pacman.