import pygame
from random import choice
from pathlib import Path



class Gourmand(pygame.sprite.Sprite):
    def __init__(self, identifier, player, x, y, max_dishes):
        super().__init__()

        # Charger le dossier contenant les ressources du jeu
        assets = Path(__file__).resolve().parent / "assets"
        self.player = player
        
        # Charger l'image normale du gourmand
        image_path = Path(__file__).resolve().parent / "assets" / "gourmand.png"
        self.image = pygame.image.load(str(image_path))
        self.image = pygame.transform.scale(self.image, (100, 100))
        
        # Definir la position du gourmand et sa hitbox
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.max_dishes = max_dishes
        #Permet de compter le nombre de plat que les gourmands ont mangé
        self.dishes_eaten = 0
        
        # Charger les pancartes correspondant aux aliments demandes
        self.desires = {"burger" : assets / "pencarte_burger.png" ,
                  "donut" : assets / "pencarte_donut.png" ,
                  "salade" : assets / "pencarte_salade.png" 
                 }
        self.signs = {}
        for food, image_path in self.desires.items():
            image = pygame.image.load(str(image_path)).convert_alpha()
            image = pygame.transform.scale(image, (55, 55))
            self.signs[food] = image
            
        self.desire = choice(list(self.desires.keys()))
        self.visible = True
        
        
        # Initialiser le mode furieux du gourmand
        self.normal_image = self.image
        image_path = Path(__file__).resolve().parent / "assets" / "gourmand_furieux.png"
        self.angry_image = pygame.image.load(str(image_path))
        self.angry_image = pygame.transform.scale(self.angry_image, (100, 100))
        self.start_time = 0
        self.angry = False
        
        
        
        # Charger les differentes barres d'enervement
        self.anger_bars = {"1" : assets / "barre_1.png" ,
                  "2" : assets / "barre_2.png" ,
                  "3" : assets / "barre_3.png" 
                 }
        self.anger_bar_images = {}
        for level, image_path in self.anger_bars.items():
            image = pygame.image.load(str(image_path)).convert_alpha()
            image = pygame.transform.scale(image, (100, 33))
            self.anger_bar_images[level] = image
        self.anger_level = 0
        self.anger_bar_visible = False
        self.killed_by_anger = False
        
        
        
            
    def eat(self):
        # Changer l'image lorsque le gourmand est rassasie ou en overdose
        if self.dishes_eaten == self.max_dishes:
            image_path = Path(__file__).resolve().parent / "assets" / "gourmand_full.png"
            self.image = pygame.image.load(str(image_path))
            self.image = pygame.transform.scale(self.image, (100, 100))

        elif self.dishes_eaten > self.max_dishes:
            image_path = Path(__file__).resolve().parent / "assets" / "gourmand_overdose.png"
            self.image = pygame.image.load(str(image_path))
            self.image = pygame.transform.scale(self.image, (100, 100))
            
            
    def draw_sign(self, screen):
        # Afficher la pancarte de l'aliment souhaite
        if not self.visible:
            return 
        image = self.signs[self.desire]
        x = self.rect.x - 22
        y = self.rect.y + 10
        
        screen.blit(image, (x,y))
            
    def update_desire(self):
        # Choisir une nouvelle envie differente de la precedente
        choices = list(self.desires.keys())
        choices.remove(self.desire)
        self.desire = choice(choices)
    
    def become_angry(self):
        # Activer temporairement l'image furieuse
        self.image = self.angry_image
        self.angry = True
        self.anger_start_time = pygame.time.get_ticks()
        
    def update_anger(self):
        # Revenir a l'image normale apres une seconde
        if self.angry:
            elapsed_time = pygame.time.get_ticks() - self.anger_start_time
            if elapsed_time > 1000:
                self.image = self.normal_image
                self.angry = False
                
    def draw_anger_bar(self, screen):
        # Afficher la barre d'enervement au-dessus du gourmand
        if not self.anger_bar_visible:
            return 
        level = str(min(self.anger_level, 3))
        image = self.anger_bar_images[level]
        x = self.rect.centerx - image.get_width() // 2
        y = self.rect.top - 38
        
        screen.blit(image, (x,y))
            
    def update_anger_bar(self):
        # Augmenter la colere et eliminer le gourmand au niveau maximal
        if self.killed_by_anger:
            return 
        self.anger_level += 1
        self.anger_bar_visible = True
        
        if self.anger_level >=3:
            self.killed_by_anger = True
            self.image = self.angry_image
            self.angry = False
            self.visible = False
    
        
        
        
        
        
        
        
