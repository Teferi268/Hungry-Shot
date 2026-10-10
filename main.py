import pygame
from mobs import Mobs
from player import Player
from gourmand import Gourmand
from projectile import Projectile
from pathlib import Path
from classement import show_home_screen, show_result_screen
import json

# Initialiser les composants de Pygame
pygame.init()
pygame.font.init()
pygame.display.init()

custom_font = pygame.font.SysFont('Impact', 30)

screen = pygame.display.set_mode((1080, 720))#permet de changer la dimension du jeu
pygame.display.set_caption("Mon premier jeu")
clock = pygame.time.Clock()#pour définir le nb de FPS

pseudo = show_home_screen(screen, clock)
if pseudo is None:
    pygame.quit()
    raise SystemExit

# Charger et redimensionner l'image de fond du jeu
background_path = Path(__file__).resolve().parent / "assets" / "background.png"
background = pygame.image.load(str(background_path))
background = pygame.transform.scale(background,(1080,720))

# Creer le joueur
player = Player() 

# Charger la configuration des gourmands
with open("config_gourmand.json", "r", encoding="utf-8") as fichier:
    data = json.load(fichier)
eaters = []

for info in data["gourmands"]:
    eaters.append(
        Gourmand(
            info["id"],
            player,
            info["x"],
            info["y"],
            info["plats_max"],
        )
    )
    
    
    
    
# Initialiser les elements d'affichage du score
font = pygame.font.Font(None, 50)

# Creer le projectile
projectile = Projectile(player)
mobs = pygame.sprite.Group()
last_mob_spawn = pygame.time.get_ticks()

score = 0
text =  custom_font.render("0", True, (0, 0, 0))
running = True
max_time = 60
start_time = pygame.time.get_ticks()
remaining_time = max_time

def handle_keyboard():
    # Recuperer les touches actives et gerer les actions du joueur
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_z]:
        player.move_up()
    if keys[pygame.K_s]:
        player.move_down()
        
    if keys[pygame.K_SPACE]:
        projectile.direction = "right"
        projectile.apparition()
        
    
def get_game_result():
    # Determiner si la partie est gagnee ou perdue
    full_count = 0
    overdose_count = 0
    for eater in eaters:
        if eater.killed_by_anger:
            return "defaite"
        if eater.dishes_eaten == eater.max_dishes:
            full_count += 1
        elif eater.dishes_eaten > eater.max_dishes:
            overdose_count += 1
            
    if overdose_count >= 2:
        return "defaite"
    elif full_count >= 4:
        return "victoire"
    return None
    
    
        

        
result = None
# Initialiser le timer de la partie
game_timer = 100
start_time = pygame.time.get_ticks()
# Boucle principale du jeu
while running:
    
    # Recuperer les evenements utilisateur
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            projectile.swap()
        if event.type == pygame.QUIT:
            running = False
    if not running :
        break
    
    handle_keyboard()
    projectile.update_projectile()

    # Faire traverser les mobs verticalement dans le couloir central.
    if pygame.time.get_ticks() - last_mob_spawn > 1000 and len(mobs) < 3:
        mob = Mobs()
        mob.mob_apparition()
        mobs.add(mob)
        last_mob_spawn = pygame.time.get_ticks()
    mobs.update()

    # Un mob touche par un projectile est casse.
    if projectile.visible:
        touched_mobs = pygame.sprite.spritecollide(projectile, mobs, dokill=True)
        if touched_mobs:
            projectile.visible = False
            projectile.rect.x = -100
            projectile.rect.y = -100
            score += 100
            text = custom_font.render(str(score), False, (0, 0, 0))
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
    remaining_time = max(0, game_timer - elapsed_time)
    if remaining_time == 0:
        result = "defaite"
        running = False
    
    for eater in eaters:
        eater.update_anger()
        # Verifier les collisions entre le projectile et les gourmands
        if projectile.visible and projectile.rect.colliderect(eater.rect):
            if eater.killed_by_anger:
                pass
            elif eater.dishes_eaten >= eater.max_dishes:
                eater.dishes_eaten += 1
                eater.eat()
                
            elif projectile.food == eater.desire:
                eater.dishes_eaten += 1
                eater.eat()
            

                score += 1000
                text = custom_font.render(str(score), False,(0,0,0))
                if eater.dishes_eaten < eater.max_dishes:
                    eater.update_desire()
                else:
                    eater.visible = False
                    
            else :   
                eater.become_angry()
                eater.update_anger_bar()
                score -= 500
                text = custom_font.render(str(score), False,(0,0,0))
                

            projectile.visible = False
            projectile.rect.x = -100
            projectile.rect.y = -100
            
        if running:
            result = get_game_result()
            if result == "victoire":
                running = False
            elif result == "defaite":
                running = False


        
    # Actualiser l'affichage du jeu
    screen.blit(background, (0, 0))
    screen.blit(player.image, player.rect)
    projectile.next_food(screen)
    # Afficher les gourmands
    for eater in eaters:
        screen.blit(eater.image, eater.rect)
    mobs.draw(screen)
    # Afficher les pancartes
    for eater in eaters:
        eater.draw_sign(screen)
    # Afficher les barres de colere
    for eater in eaters:
        eater.draw_anger_bar(screen)
    


    if projectile.visible:
        screen.blit(projectile.image, projectile.rect)
    screen.blit(text, (0,0))
    pygame.display.flip()
    # Afficher le timer avec une couleur selon le temps restant
    font_timer = pygame.font.SysFont("Impact", 60)
    if remaining_time > 20:
        couleur = (255, 255, 255)
    elif remaining_time > 10:
        couleur = (255, 190, 60)
    else:
        couleur = (255, 65, 65)
    texte_timer = custom_font.render(
        f"Temps : {remaining_time}s",
        True,
        couleur
    )

    # Ajouter un contour noir pour rendre le timer lisible
    contour_timer = custom_font.render(
        f"Temps : {remaining_time}s",
        True,
        (0, 0, 0)
    )

    x_timer = 450
    y_timer = 20

    for dx, dy in [
        (-2, 0),
        (2, 0),
        (0, -2),
        (0, 2)
    ]:

        screen.blit(
            contour_timer,
            (x_timer + dx, y_timer + dy)
        )

    screen.blit(
        texte_timer,
        (x_timer, y_timer)
    )


    pygame.display.flip()
    clock.tick(60)



if result in ("victoire", "defaite"):

    # Calculer la duree reelle de la partie
    game_duration = (
        pygame.time.get_ticks() - start_time
    ) // 1000

    # Afficher le score final et le classement
    show_result_screen(
        screen,
        clock,
        pseudo,
        score,
        game_duration,
        result
    )


pygame.quit()
