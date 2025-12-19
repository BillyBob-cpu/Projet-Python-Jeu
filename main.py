import pygame
import sys
import random
import math
from src.models.player import Player
from src.models.map import Map
from src.models.artifact import Artifact
from src.models.enemy import Enemy
from src.utils.score_manager import load_high_score, save_high_score

def place_enemy_far(enemy, map_obj, player):
    """Place un ennemi sur une case vide ET loin du joueur"""
    valid_spots = map_obj.get_empty_spots()
    
    safe_spots = []
    for spot in valid_spots:
        dist_x = spot[0] - player.rect.x
        dist_y = spot[1] - player.rect.y
        distance = math.sqrt(dist_x**2 + dist_y**2)
        
        if distance > 300: 
            safe_spots.append(spot)
    
    if safe_spots:
        enemy.rect.topleft = random.choice(safe_spots)
    elif valid_spots:
        enemy.rect.topleft = random.choice(valid_spots)

def place_object_safely(sprite, map_obj):
    valid_spots = map_obj.get_empty_spots()
    if valid_spots:
        sprite.rect.topleft = random.choice(valid_spots)

def draw_ui(screen, score, high_score, level):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    high_score_text = font.render(f"Record: {high_score}", True, (255, 215, 0))
    level_text = font.render(f"Niveau: {level}", True, (100, 200, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 40))
    screen.blit(level_text, (10, 70))

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Archéologie & Enigmes")
    clock = pygame.time.Clock()

    game_map = Map()
    all_sprites = pygame.sprite.Group()
    artifacts_group = pygame.sprite.Group()
    enemies_group = pygame.sprite.Group()

    player = Player(0, 0)
    all_sprites.add(player)

    treasure = Artifact(0, 0)
    artifacts_group.add(treasure)
    all_sprites.add(treasure)

    score = 0
    high_score = load_high_score()
    game_state = "playing"
    
    speed_boosted = False
    level_2_unlocked = False
    level_3_unlocked = False

    font_end = pygame.font.Font(None, 74)
    font_sub = pygame.font.Font(None, 36)

    def reset_game():
        nonlocal score, speed_boosted, level_2_unlocked, level_3_unlocked, game_state
        score = 0
        speed_boosted = False
        level_2_unlocked = False
        level_3_unlocked = False
        game_state = "playing"
        
        game_map.load_level(1)
        player.rect.topleft = (96, 96)
        place_object_safely(treasure, game_map)
        
        enemies_group.empty()
        mummy = Enemy(0, 0)
        place_enemy_far(mummy, game_map, player)
        enemies_group.add(mummy)
        
        all_sprites.empty()
        all_sprites.add(player, treasure, mummy)

    reset_game()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if game_state != "playing":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        running = False

        if game_state == "playing":
            
            if score >= 130:
                game_state = "victory"
                save_high_score(score)

            # Boost Vitesse (Niveau 1 -> 30 pts)
            if score >= 30 and not speed_boosted:
                for enemy in enemies_group:
                    enemy.speed += 1
                speed_boosted = True

            # NIVEAU 2 (60 pts) : Rapides
            if score >= 60 and not level_2_unlocked:
                game_map.load_level(2)
                level_2_unlocked = True
                
                player.rect.topleft = (96, 96)
                place_object_safely(treasure, game_map)
                
                enemies_group.empty()
                for _ in range(2):
                    m = Enemy(0, 0)
                    place_enemy_far(m, game_map, player)
                    enemies_group.add(m)
                
                all_sprites.empty()
                all_sprites.add(player, treasure)
                all_sprites.add(enemies_group)
                
                # On applique le boost pour le niveau 2
                if speed_boosted:
                    for enemy in enemies_group: enemy.speed += 1

            # NIVEAU 3 (90 pts) : LENTES MAIS NOMBREUSES
            if score >= 90 and not level_3_unlocked:
                game_map.load_level(3)
                level_3_unlocked = True
                
                player.rect.topleft = (96, 96)
                place_object_safely(treasure, game_map)
                
                enemies_group.empty()
                for _ in range(3):
                    m = Enemy(0, 0)
                    place_enemy_far(m, game_map, player)
                    # IMPORTANT : On NE met PAS le boost de vitesse ici
                    # Elles restent à la vitesse de base (2)
                    enemies_group.add(m)
                    
                all_sprites.empty()
                all_sprites.add(player, treasure)
                all_sprites.add(enemies_group)
                
                print("Niveau 3 : Vitesse normale pour les momies !")

            player.update(game_map.walls)
            enemies_group.update(player, game_map.walls)
            
            hits = pygame.sprite.spritecollide(player, artifacts_group, False)
            for hit in hits:
                score += 10
                save_high_score(score)
                place_object_safely(hit, game_map)

            if pygame.sprite.spritecollideany(player, enemies_group):
                game_state = "game_over"
                save_high_score(score)

        if game_state == "playing":
            game_map.draw(screen)
            all_sprites.draw(screen)
            draw_ui(screen, score, high_score, game_map.current_level)
            
        elif game_state == "game_over":
            screen.fill((0, 0, 0))
            text = font_end.render("GAME OVER", True, (255, 0, 0))
            sub_text = font_sub.render(f"ESPACE: Rejouer  |  ECHAP: Quitter", True, (255, 255, 255))
            screen.blit(text, (800//2 - text.get_width()//2, 600//2 - 50))
            screen.blit(sub_text, (800//2 - sub_text.get_width()//2, 600//2 + 20))

        elif game_state == "victory":
            screen.fill((0, 0, 0))
            text = font_end.render("VICTOIRE !", True, (0, 255, 0))
            sub_text = font_sub.render(f"ESPACE: Rejouer  |  ECHAP: Quitter", True, (255, 255, 255))
            screen.blit(text, (800//2 - text.get_width()//2, 600//2 - 50))
            screen.blit(sub_text, (800//2 - sub_text.get_width()//2, 600//2 + 20))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()