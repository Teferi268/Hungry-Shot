import pygame
from pathlib import Path


class Mobs(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Charger et redimensionner l'image du joueur
        #Charger l'image du joueur
        image_path = Path(__file__).resolve().parent / "assets" / "cuistot.png"
        self.image = pygame.image.load(str(image_path))
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.pannel_spawn = [300,500]
        
        # Definir la position du joueur et sa hitbox
        #Position du joueur + hitbox
        self.rect = self.image.get_rect()
        self.rect.x = pygame.choice(self.pannel_spawn[0], self.pannel_spawn[1])
        self.rect.y = - 720
        
    def move_up(self):
        # Deplacer le joueur vers le haut
        self.rect.y -= 4
        
    def move_down(self):
        # Deplacer le joueur vers le bas
        self.rect.y += 4
