import pygame
from random import choice
from pathlib import Path


class Mobs(pygame.sprite.Sprite):
    mobs_bank = None

    def __init__(self):
        super().__init__()

        # Charger les images des mobs
        assets = Path(__file__).resolve().parent / "assets"
        self.mobs = {"piment": assets / "piment.png",
                     "fromage": assets / "fromage.png",
                     "rat": assets / "rat.png",
                     "oignon": assets / "oignon.png"}
        if Mobs.mobs_bank is None:
            Mobs.mobs_bank = {}
            for mob, image_path in self.mobs.items():
                image = pygame.image.load(str(image_path)).convert_alpha()
                Mobs.mobs_bank[mob] = pygame.transform.scale(image, (55, 55))
        self.mobs_bank = Mobs.mobs_bank

        self.mob = choice(list(self.mobs.keys()))
        self.image = self.mobs_bank[self.mob]
        self.visible = False
        # Le couloir se trouve entre le cuistot et les gourmands.
        self.pannel_spawn_x = [300, 500, 700]
        self.pannel_spawn_y = [720, -55]
        self.speed = 8

        # Definir la position du mob et sa hitbox
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def move_up(self):
        # Deplacer le mob vers le haut
        self.rect.y -= self.speed

    def move_down(self):
        # Deplacer le mob vers le bas
        self.rect.y += self.speed

    def choice_mob(self):
        # Choisir un mob different du precedent
        choices = list(self.mobs.keys())
        choices.remove(self.mob)
        self.mob = choice(choices)
        self.image = self.mobs_bank[self.mob]
        self.rect = self.image.get_rect(topleft=self.rect.topleft)

    def mob_apparition(self):
        # Faire apparaitre le mob en haut ou en bas de l'ecran
        if self.visible:
            return

        self.choice_mob()
        self.visible = True
        self.rect.x = choice(list(self.pannel_spawn_x))
        self.rect.y = choice(list(self.pannel_spawn_y))
        self.spawn_y = self.rect.y

    def mob_update(self):
        # Faire traverser le mob verticalement dans le couloir
        if not self.visible:
            return

        if self.spawn_y > 0:
            self.move_up()
        else:
            self.move_down()

        if self.rect.bottom < 0 or self.rect.top > 720:
            self.visible = False
            self.kill()

    def update(self):
        self.mob_update()
