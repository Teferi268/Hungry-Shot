#Tout la partie affichage est fait par ia, 

import pygame
import json
from pathlib import Path
from datetime import datetime

SCORES_FILE = Path(__file__).resolve().parent / "scores.json"

WIDTH = 1080
HEIGHT = 720

BACKGROUND = (38, 32, 29)
WHITE = (255, 245, 225)
GOLD = (245, 197, 66)
GREY = (175, 165, 155)
RED = (230, 80, 65)


def load_scores():
    # Charger les scores existants depuis le fichier JSON
    if not SCORES_FILE.exists():
        return []

    try:
        with open(SCORES_FILE, "r", encoding="utf-8") as file:
            scores = json.load(file)

        if isinstance(scores, list):
            return scores

    except (json.JSONDecodeError, OSError):
        pass

    return []


def save_score(username, score, duration, result):
    # Ajouter la partie actuelle aux scores existants
    scores = load_scores()

    new_game = {
        "pseudo": username,
        "score": score,
        "temps": duration,
        "resultat": result,
        "date": datetime.now().strftime("%d/%m/%Y %H:%M")
    }

    scores.append(new_game)

    with open(SCORES_FILE, "w", encoding="utf-8") as file:
        json.dump(scores, file, indent=4, ensure_ascii=False)


def get_ranking():
    # Trier les scores du meilleur au moins bon
    scores = load_scores()

    # Meilleur score en premier
    # En cas d'égalité, le plus rapide gagne
    return sorted(
        scores,
        key=lambda game: (
            -game["score"],
            game["temps"]
        )
    )


def format_time(seconds):
    # Convertir un nombre de secondes en minutes et secondes
    minutes = seconds // 60
    remaining_seconds = seconds % 60

    return f"{minutes:02d}:{remaining_seconds:02d}"


def draw_text(screen, text, size, color, x, y):
    # Creer puis afficher un texte centre a la position indiquee
    font = pygame.font.SysFont("Impact", size)
    surface = font.render(str(text), True, color)
    rect = surface.get_rect(center=(x, y))

    screen.blit(surface, rect)


def draw_ranking(screen, start_y=370):
    # Afficher les cinq meilleurs scores
    best_scores = get_ranking()[:5]

    draw_text(screen, "TOP 5 DES JOUEURS", 35, GOLD, 540, start_y)

    if not best_scores:
        draw_text(
            screen,
            "Aucune partie enregistree",
            24, GREY, 540, start_y + 50
        )
        return

    for position, game in enumerate(best_scores, start=1):
        y = start_y + 45 + (position - 1) * 42

        line = (
            f"{position}. {game['pseudo']}     "
            f"{game['score']} pts     "
            f"{format_time(game['temps'])}"
        )

        color = GOLD if position == 1 else WHITE

        draw_text(screen, line, 24, color, 540, y)


def show_home_screen(screen, clock):
    # Afficher le menu d'accueil et recuperer le pseudo du joueur
    username = ""
    active = True

    while active:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]

                elif event.key == pygame.K_RETURN:
                    if username.strip():
                        return username.strip()

                elif len(username) < 15 and event.unicode.isprintable():
                    username += event.unicode

        screen.fill(BACKGROUND)

        draw_text(screen, "HUNGRY GAME", 75, GOLD, 540, 85)

        draw_text(
            screen,
            "Entre ton pseudo :",
            30, WHITE, 540, 175
        )

        # Zone de saisie
        pygame.draw.rect(
            screen, (255, 242, 213), (340, 220, 400, 60),
            border_radius=8
        )

        draw_text(
            screen,
            username + "|",
            30, BACKGROUND, 540, 250
        )

        draw_text(
            screen,
            "Appuie sur ENTREE pour jouer",
            25, GOLD, 540, 320
        )

        draw_ranking(screen, 390)

        pygame.display.flip()
        clock.tick(60)


def show_result_screen(screen, clock, username, score, duration, result):
    # Sauvegarder la partie une seule fois avant d'afficher le resultat
    save_score(username, score, duration, result)

    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    return

        screen.fill(BACKGROUND)

        if result == "victoire":
            titre = "VICTOIRE !"
            color = GOLD
        else:
            titre = "GAME OVER"
            color = RED

        draw_text(screen, titre, 65, color, 540, 65)

        draw_text(
            screen, f"Joueur : {username}",
            30, WHITE, 540, 140
        )

        draw_text(
            screen, f"Score : {score} points",
            35, GOLD, 540, 195
        )

        draw_text(
            screen, f"Temps : {format_time(duration)}",
            30, WHITE, 540, 245
        )

        draw_ranking(screen, 320)

        draw_text(
            screen,
            "ENTREE ou ECHAP pour quitter",
            22, GREY, 540, 640
        )

        pygame.display.flip()
        clock.tick(60)
