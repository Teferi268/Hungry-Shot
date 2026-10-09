import pygame
from pathlib import Path


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Charger et redimensionner l'image du joueur
        #Charger l'image du joueur
        image_path = Path(__file__).resolve().parent / "assets" / "cuistot.png"
        self.image = pygame.image.load(str(image_path))
        self.image = pygame.transform.scale(self.image, (100, 100))
        
        # Definir la position du joueur et sa hitbox
        #Position du joueur + hitbox
        self.rect = self.image.get_rect()
        self.rect.width - 100
        self.rect.height - 100
        self.rect.x = 100
        self.rect.y = 340
        
    def move_up(self):
        # Deplacer le joueur vers le haut
        self.rect.y -= 4
        
    def move_down(self):
        # Deplacer le joueur vers le bas
        self.rect.y += 4

