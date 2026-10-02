"""STAY CLEAN — a small Pygame game about dodging dirt."""

from __future__ import annotations

import math
import random
import sys

import pygame


WIDTH, HEIGHT = 960, 640
FPS = 60
WIN_TIME = 45
MAX_DIRT = 5
SKY = (177, 226, 255)
GRASS = (104, 190, 91)
BROWN = (104, 60, 28)
DARK_BROWN = (72, 38, 19)
CREAM = (255, 237, 204)
BLACK = (33, 33, 42)
RED = (219, 69, 66)



def new_game() -> dict:
    """Make a fresh collection of values for one round."""
    return {
        "player": pygame.Rect(WIDTH // 2 - 24, HEIGHT - 105, 48, 68),
        "poops": [],
        "score": 0,
        "dirt": 0,
        "spawn_timer": 0.0,
        "elapsed": 0.0,
        "message": "",
        "message_timer": 0.0,
        "hit_flash": 0.0,
        "state": "start",
    }


def spawn_poop(game: dict) -> None:
    """Add one falling poop at a random horizontal position."""
    size = random.randint(34, 54)
    speed_boost = min(int(game["elapsed"] * 4), 145)
    game["poops"].append(
        {
            "rect": pygame.Rect(random.randint(15, WIDTH - size - 15), -size, size, size),
            "speed": random.randint(185, 260) + speed_boost,
            "phase": random.random() * math.tau,
        }
    )


def move_player(player: pygame.Rect, keys: pygame.key.ScancodeWrapper, dt: float) -> None:
    """Move the player with the arrow keys or WASD, staying on the screen."""
    horizontal = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(
        keys[pygame.K_LEFT] or keys[pygame.K_a]
    )
    vertical = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(
        keys[pygame.K_UP] or keys[pygame.K_w]
    )
    if horizontal and vertical:
        horizontal *= 0.707
        vertical *= 0.707

    player.x += int(horizontal * 330 * dt)
    player.y += int(vertical * 330 * dt)
    player.clamp_ip(pygame.Rect(12, 195, WIDTH - 24, HEIGHT - 212))

def ew():
    return "EW!"


def update_poops(game: dict, dt: float) -> None:
    """Move hazards down, score dodges, and make the player dirty on a hit."""
    player = game["player"]
    for poop in game["poops"][:]:
        poop["phase"] += dt * 4
        poop["rect"].x += int(math.sin(poop["phase"]) * 18 * dt)
        poop["rect"].y += int(poop["speed"] * dt)

        if poop["rect"].colliderect(player):
            game["message"] = ew()
            game["poops"].remove(poop)
            game["dirt"] += 1
            game["message_timer"] = 0.9
            game["hit_flash"] = 0.23
        elif poop["rect"].top > HEIGHT:
            game["poops"].remove(poop)
            game["score"] += 10


def draw_background(surface: pygame.Surface) -> None:
    """Draw a simple sunny field."""
    surface.fill(SKY)
    pygame.draw.circle(surface, (255, 224, 92), (850, 84), 45)
    pygame.draw.rect(surface, GRASS, (0, 185, WIDTH, HEIGHT - 185))
    for x in range(0, WIDTH, 80):
        pygame.draw.line(surface, (88, 174, 80), (x, HEIGHT), (x + 38, 555), 3)


def draw_poop(surface: pygame.Surface, rect: pygame.Rect) -> None:
    """Draw one cartoon poop using only Pygame shapes."""
    pygame.draw.ellipse(surface, DARK_BROWN, rect.inflate(4, 2))
    pygame.draw.ellipse(surface, BROWN, (rect.x, rect.y + rect.height * 0.56, rect.width, rect.height * 0.42))
    pygame.draw.ellipse(surface, BROWN, (rect.x + rect.width * 0.14, rect.y + rect.height * 0.28, rect.width * 0.72, rect.height * 0.44))
    pygame.draw.circle(surface, BROWN, (rect.centerx, rect.y + int(rect.height * 0.27)), int(rect.width * 0.25))
    pygame.draw.circle(surface, CREAM, (rect.x + int(rect.width * 0.34), rect.y + int(rect.height * 0.58)), 3)
    pygame.draw.circle(surface, CREAM, (rect.x + int(rect.width * 0.67), rect.y + int(rect.height * 0.58)), 3)


def draw_player(surface: pygame.Surface, player: pygame.Rect, dirt: int) -> None:
    """Draw the player, adding more brown splats as their dirt meter rises."""
    pygame.draw.line(surface, BLACK, (player.x + 13, player.bottom - 10), (player.x + 9, player.bottom + 6), 5)
    pygame.draw.line(surface, BLACK, (player.right - 13, player.bottom - 10), (player.right - 9, player.bottom + 6), 5)
    pygame.draw.rect(surface, (60, 119, 218), (player.x + 6, player.y + 29, player.width - 12, 30), border_radius=7)
    pygame.draw.circle(surface, CREAM, (player.centerx, player.y + 21), 19)
    pygame.draw.circle(surface, BLACK, (player.centerx - 7, player.y + 18), 2)
    pygame.draw.circle(surface, BLACK, (player.centerx + 7, player.y + 18), 2)
    pygame.draw.arc(surface, BLACK, (player.centerx - 8, player.y + 19, 16, 12), 0, math.pi, 2)
    pygame.draw.arc(surface, DARK_BROWN, (player.x + 5, player.y - 1, player.width - 10, 28), math.pi, math.tau, 7)

    splats = ((12, 35, 5), (33, 49, 6), (19, 15, 4), (38, 26, 4), (7, 56, 4))
    for x, y, radius in splats[:dirt]:
        pygame.draw.circle(surface, BROWN, (player.x + x, player.y + y), radius)
        pygame.draw.circle(surface, DARK_BROWN, (player.x + x - 1, player.y + y - 1), max(1, radius - 3))


def draw_text(surface: pygame.Surface, text: str, size: int, pos: tuple[int, int], color: tuple[int, int, int] = BLACK) -> None:
    """Draw centered text at a position."""
    font = pygame.font.SysFont("arial", size, bold=True)
    image = font.render(text, True, color)
    surface.blit(image, image.get_rect(center=pos))


def draw_game(surface: pygame.Surface, game: dict) -> None:
    """Draw the field, the player, hazards, score, and dirt meter."""
    draw_background(surface)
    for poop in game["poops"]:
        draw_poop(surface, poop["rect"])
    draw_player(surface, game["player"], game["dirt"])
    draw_text(surface, f"Score: {game['score']}", 28, (90, 35))
    seconds_left = max(0, math.ceil(WIN_TIME - game["elapsed"]))
    draw_text(surface, f"Survive: {seconds_left}s", 24, (WIDTH // 2, 35))
    draw_text(surface, "Dirt:", 25, (790, 34))
    for number in range(5):
        color = BROWN if number < game["dirt"] else CREAM
        pygame.draw.circle(surface, color, (855 + number * 21, 34), 8)

    if game["message_timer"] > 0:
        draw_text(surface, game["message"], 44, (game["player"].centerx, game["player"].y - 35), RED)

    if game["hit_flash"] > 0:
        flash = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        flash.fill((222, 97, 54, 90))
        surface.blit(flash, (0, 0))


def draw_start_screen(surface: pygame.Surface) -> None:
    """Explain the goal before the first round starts."""
    draw_text(surface, "STAY CLEAN", 58, (WIDTH // 2, 98), RED)
    draw_text(surface, "Avoid the falling poop for 45 seconds", 29, (WIDTH // 2, 140))
    draw_text(surface, "Move with arrow keys or WASD", 26, (WIDTH // 2, HEIGHT - 78))
    draw_text(surface, "Press SPACE to start", 26, (WIDTH // 2, HEIGHT - 43), BLACK)


def draw_end_screen(surface: pygame.Surface, game: dict) -> None:
    """Show either a victory or a defeat message over the final game frame."""
    shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    shade.fill((14, 23, 35, 175))
    surface.blit(shade, (0, 0))

    if game["state"] == "win":
        draw_text(surface, "YOU STAYED CLEAN!", 52, (WIDTH // 2, 255), (255, 235, 111))
        draw_text(surface, f"Final score: {game['score']}", 30, (WIDTH // 2, 303), CREAM)
    else:
        draw_text(surface, "TOO STINKY!", 55, (WIDTH // 2, 255), (255, 153, 110))
        draw_text(surface, "Five splats was one too many.", 28, (WIDTH // 2, 303), CREAM)

    draw_text(surface, "Press R to try again", 27, (WIDTH // 2, 362), CREAM)


def smoke_test() -> None:
    """Check that Pygame can draw a frame and register a collision."""
    pygame.init()
    surface = pygame.display.set_mode((WIDTH, HEIGHT))
    game = new_game()
    spawn_poop(game)
    draw_game(surface, game)
    game["poops"] = [{"rect": game["player"].copy(), "speed": 0, "phase": 0.0}]
    update_poops(game, 0.0)
    assert game["dirt"] == 1, "A collision should make the player dirtier."
    game["state"] = "win"
    draw_end_screen(surface, game)
    game["state"] = "lose"
    draw_end_screen(surface, game)
    pygame.quit()
    print("Smoke test passed: Pygame drew, detected a collision, and showed both end screens.")


def main() -> None:
    """Run the game until the player closes its window."""
    pygame.init()
    pygame.display.set_caption("STAY CLEAN")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    game = new_game()
    running = True

    while running:
        dt = clock.tick(FPS) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and game["state"] == "start":
                game["state"] = "playing"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r and game["state"] in ("win", "lose"):
                game = new_game()
                game["state"] = "playing"

        if game["state"] == "playing":
            move_player(game["player"], pygame.key.get_pressed(), dt)
            game["message_timer"] = max(0.0, game["message_timer"] - dt)
            game["hit_flash"] = max(0.0, game["hit_flash"] - dt)
            game["spawn_timer"] -= dt
            if game["spawn_timer"] <= 0:
                spawn_poop(game)
                game["spawn_timer"] = max(0.34, 0.78 - game["elapsed"] * 0.009)
            update_poops(game, dt)
            game["elapsed"] += dt
            if game["dirt"] >= MAX_DIRT:
                game["state"] = "lose"
            elif game["elapsed"] >= WIN_TIME:
                game["state"] = "win"

        draw_game(screen, game)
        if game["state"] == "start":
            draw_start_screen(screen)
        elif game["state"] in ("win", "lose"):
            draw_end_screen(screen, game)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    if "--smoke-test" in sys.argv:
        smoke_test()
    else:
        main()
