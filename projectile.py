import pygame
from random import randint
import time
from pathlib import Path


class Projectile(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()

        # Charger les images des aliments et leurs versions miniatures
        assets = Path(__file__).resolve().parent / "assets"
        self.projectiles = [assets / "burger.png", assets / "donut.png", assets / "salade.png"]
        self.mini_projectiles = [assets / "burger_mini.png", assets / "donut_mini.png", assets / "salade_mini.png"]
        self.foods = ["burger", "donut", "salade"]
        self.food = "burger"
        self.index = 1 
        
        
        # Charger l'image du projectile actuel
        self.image = pygame.image.load(str(self.projectiles[0]))
        self.image = pygame.transform.scale(self.image, (60, 60))
        
        # Charger l'image miniature affichee au-dessus du joueur
        self.mini_image = pygame.image.load(str(self.mini_projectiles[0]))
        self.mini_image = pygame.transform.scale(self.mini_image, (40, 40))
        
        
        # Initialiser la position et l'etat du projectile
        self.rect = self.image.get_rect()
        self.rect.x = 600
        self.rect.y = 500 
        self.visible = True
        self.start_time = 0
        self.direction = "right"
        
        self.player = player
        
    def apparition(self):
        # Faire apparaitre le projectile a la position du joueur
        if self.visible:
            return
        self.rect.x = self.player.rect.x
        self.rect.y = self.player.rect.y
        self.visible = True
        self.start_time = pygame.time.get_ticks()
        
        
    def update_projectile(self):
        # Faire avancer le projectile et le masquer apres trois secondes
        if self.visible:
            if self.direction == "right":
                self.rect.x +=40
            elapsed_time = pygame.time.get_ticks() - self.start_time
            if elapsed_time > 3000:
                self.visible = False
    def swap(self):
        # Passer a l'aliment suivant
        nom_image = self.projectiles[self.index]
        self.food = self.foods[self.index]
        image_path = nom_image
        self.image = pygame.image.load(str(image_path))
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.mini_image = pygame.image.load(str(image_path))
        self.mini_image = pygame.transform.scale(self.mini_image, (100, 100))
        self.index = (self.index + 1) % len(self.projectiles)
        
    def next_food(self, screen):
        # Afficher le prochain aliment disponible
        image_path = self.mini_projectiles[self.index-1]
        
        self.mini_image = pygame.image.load(str(image_path))
        self.mini_image = pygame.transform.scale(self.mini_image, (40, 40))
        
        x = self.player.rect.x
        y = self.player.rect.y
        
        screen.blit(self.mini_image, (x, y))
        
        
        
    
