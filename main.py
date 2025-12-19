import pygame
import sys
import random
import math
import os
from src.models.player import Player
from src.models.map import Map
from src.models.artifact import Artifact
from src.models.enemy import Enemy
from src.utils.score_manager import load_high_score, save_high_score

def place_enemy_far(enemy, map_obj, player):
    valid_spots = map_obj.get_empty_spots()
    safe_spots = []
    for spot in valid_spots:
        dist_x = spot[0] - player.rect.x
        dist_y = spot[1] - player.rect.y
        distance = math.sqrt(dist_x**2 + dist_y**2)
        if distance > 300: 
            safe_spots.append(spot)
    
    if safe_spots: enemy.rect.topleft = random.choice(safe_spots)
    elif valid_spots: enemy.rect.topleft = random.choice(valid_spots)

def place_object_safely(sprite, map_obj):
    valid_spots = map_obj.get_empty_spots()
    if valid_spots: sprite.rect.topleft = random.choice(valid_spots)

current_track = None

def play_music(track_name):
    global current_track
    if current_track == track_name:
        return

    possible_paths = [
        f"assets/music/{track_name}",
        f"music/{track_name}",
        f"assets/music/{track_name.lower()}",
        f"assets/music/{track_name.capitalize()}"
    ]
    
    found_path = None
    for path in possible_paths:
        if os.path.exists(path):
            found_path = path
            break
            
    if found_path:
        try:
            pygame.mixer.music.load(found_path)
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(1.0)
            current_track = track_name
        except Exception:
            pass

def draw_ui(screen, score, high_score, level):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    high_score_text = font.render(f"Record: {high_score}", True, (255, 215, 0))
    level_text = font.render(f"Niveau: {level}", True, (100, 200, 255))
    if level == 4: level_text = font.render(f"Niveau: BOSS FINAL", True, (255, 50, 50))
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 40))
    screen.blit(level_text, (10, 70))

def main():
    pygame.init()
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Relic Hunter: Egypt")
    clock = pygame.time.Clock()

    try:
        menu_bg = pygame.image.load("assets/images/home.jpg").convert()
        menu_bg = pygame.transform.scale(menu_bg, (800, 600))
    except FileNotFoundError:
        try:
            menu_bg = pygame.image.load("assets/images/home.png").convert()
            menu_bg = pygame.transform.scale(menu_bg, (800, 600))
        except:
            menu_bg = pygame.Surface((800, 600))
            menu_bg.fill((30, 30, 30))

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
    
    game_state = "menu"
    play_music("Level_1.mp3")
    
    speed_boosted = False
    level_2_unlocked = False
    level_3_unlocked = False
    level_4_unlocked = False

    target_riddle_level = 1 

    font_title = pygame.font.Font(None, 100)
    font_button = pygame.font.Font(None, 50)
    font_riddle = pygame.font.Font(None, 40)
    font_input = pygame.font.Font(None, 60)
    font_end = pygame.font.Font(None, 74)
    font_sub = pygame.font.Font(None, 36)

    riddle_input = ""
    riddle_error = ""

    def start_level_1():
        nonlocal score, speed_boosted, level_2_unlocked, level_3_unlocked, level_4_unlocked, game_state, treasure
        score = 0
        speed_boosted = False
        level_2_unlocked = False
        level_3_unlocked = False
        level_4_unlocked = False
        game_state = "playing"
        
        play_music("Level_1.mp3")
        
        game_map.load_level(1)
        player.rect.topleft = (96, 96)
        
        treasure.kill()
        treasure = Artifact(0, 0, is_final_treasure=False)
        artifacts_group.add(treasure)
        all_sprites.add(treasure)
        place_object_safely(treasure, game_map)
        
        enemies_group.empty()
        mummy = Enemy(0, 0)
        place_enemy_far(mummy, game_map, player)
        enemies_group.add(mummy)
        
        all_sprites.empty()
        all_sprites.add(player, treasure, mummy)

    def load_level_2():
        nonlocal level_2_unlocked, game_state, speed_boosted
        game_map.load_level(2)
        level_2_unlocked = True
        game_state = "playing"
        play_music("Level_2.mp3")
        player.rect.topleft = (96, 96)
        place_object_safely(treasure, game_map)
        enemies_group.empty()
        for _ in range(2):
            m = Enemy(0, 0)
            place_enemy_far(m, game_map, player)
            enemies_group.add(m)
        all_sprites.empty()
        all_sprites.add(player, treasure, enemies_group)
        if speed_boosted:
            for enemy in enemies_group: enemy.speed += 1

    def load_level_3():
        nonlocal level_3_unlocked, game_state
        game_map.load_level(3)
        level_3_unlocked = True
        game_state = "playing"
        play_music("Level_3.mp3")
        player.rect.topleft = (96, 96)
        place_object_safely(treasure, game_map)
        enemies_group.empty()
        for _ in range(3):
            m = Enemy(0, 0)
            place_enemy_far(m, game_map, player)
            enemies_group.add(m)
        all_sprites.empty()
        all_sprites.add(player, treasure, enemies_group)

    def load_level_4():
        nonlocal level_4_unlocked, game_state, treasure
        game_map.load_level(4)
        level_4_unlocked = True
        game_state = "playing"
        play_music("Level_boss.mp3")
        place_object_safely(player, game_map)
        treasure.kill()
        treasure = Artifact(0, 0, is_final_treasure=True)
        artifacts_group.add(treasure)
        all_sprites.add(treasure)
        place_object_safely(treasure, game_map)
        enemies_group.empty()
        boss = Enemy(600, 500, is_boss=True)
        enemies_group.add(boss)
        all_sprites.empty()
        all_sprites.add(player, treasure, boss)

    button_rect = pygame.Rect(300, 400, 200, 60)

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if game_state == "menu":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(mouse_pos):
                        game_state = "riddle"
                        target_riddle_level = 1
                        riddle_input = ""
                        riddle_error = ""

            elif game_state == "riddle":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        user_ans = riddle_input.lower().strip()
                        
                        success = False
                        if target_riddle_level == 1:
                            if "cleopatre" in user_ans or "cléopâtre" in user_ans:
                                start_level_1()
                                success = True
                        elif target_riddle_level == 2:
                            if "pyramide" in user_ans:
                                load_level_2()
                                success = True
                        elif target_riddle_level == 3:
                            if "nil" in user_ans:
                                load_level_3()
                                success = True
                        elif target_riddle_level == 4:
                            if "sphinx" in user_ans:
                                load_level_4()
                                success = True
                        
                        if not success:
                            riddle_error = "Mauvaise réponse !"
                            riddle_input = ""
                            
                    elif event.key == pygame.K_BACKSPACE:
                        riddle_input = riddle_input[:-1]
                    else:
                        if len(riddle_input) < 20:
                            riddle_input += event.unicode

            elif game_state != "playing":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_state = "riddle"
                        target_riddle_level = 1
                        riddle_input = ""
                        riddle_error = ""
                    elif event.key == pygame.K_ESCAPE: running = False

        if game_state == "menu":
            screen.blit(menu_bg, (0, 0))
            
            title_surf = font_title.render("RELIC HUNTER", True, (255, 215, 0))
            subtitle_surf = font_button.render("EGYPT", True, (255, 255, 255))
            screen.blit(title_surf, (400 - title_surf.get_width()//2, 100))
            screen.blit(subtitle_surf, (400 - subtitle_surf.get_width()//2, 180))
            
            if button_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (255, 255, 0), button_rect)
                text_color = (0, 0, 0)
            else:
                pygame.draw.rect(screen, (200, 150, 0), button_rect)
                text_color = (255, 255, 255)
            
            pygame.draw.rect(screen, (255, 255, 255), button_rect, 3)
            btn_text = font_button.render("JOUER", True, text_color)
            screen.blit(btn_text, (button_rect.centerx - btn_text.get_width()//2, button_rect.centery - btn_text.get_height()//2))

        elif game_state == "riddle":
            screen.blit(menu_bg, (0, 0))
            
            overlay = pygame.Surface((700, 400))
            overlay.set_alpha(220)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (50, 100))
            
            lines = []
            if target_riddle_level == 1:
                lines = ["Je suis la derniere reine d'Egypte.", "Amante de Cesar.", "Qui suis-je ?"]
            elif target_riddle_level == 2:
                lines = ["Je suis un tombeau triangulaire.", "Je pointe vers le ciel.", "Qui suis-je ?"]
            elif target_riddle_level == 3:
                lines = ["Je suis le plus long fleuve.", "Je traverse toute l'Egypte.", "Qui suis-je ?"]
            elif target_riddle_level == 4:
                lines = ["Gardien des pyramides.", "Corps de lion, tete d'homme.", "Qui suis-je ?"]
            
            y_offset = 120
            for line in lines:
                text = font_riddle.render(line, True, (255, 215, 0))
                screen.blit(text, (400 - text.get_width()//2, y_offset))
                y_offset += 40
            
            pygame.draw.rect(screen, (255, 255, 255), (200, 350, 400, 60), 2)
            input_surf = font_input.render(riddle_input, True, (255, 255, 255))
            screen.blit(input_surf, (400 - input_surf.get_width()//2, 360))
            
            if riddle_error:
                err_surf = font_sub.render(riddle_error, True, (255, 50, 50))
                screen.blit(err_surf, (400 - err_surf.get_width()//2, 430))
            
            hint = font_sub.render("(Ecris la reponse et tape ENTREE)", True, (200, 200, 200))
            screen.blit(hint, (400 - hint.get_width()//2, 500))

        elif game_state == "playing":
            
            if score >= 180:
                game_state = "victory"
                save_high_score(score)
                pygame.mixer.music.stop()

            if score >= 30 and not speed_boosted:
                for enemy in enemies_group: enemy.speed += 1
                speed_boosted = True

            if score >= 60 and not level_2_unlocked:
                game_state = "riddle"
                target_riddle_level = 2
                riddle_input = ""
                riddle_error = ""

            if score >= 90 and not level_3_unlocked:
                game_state = "riddle"
                target_riddle_level = 3
                riddle_input = ""
                riddle_error = ""

            if score >= 130 and not level_4_unlocked:
                game_state = "riddle"
                target_riddle_level = 4
                riddle_input = ""
                riddle_error = ""

            player.update(game_map.walls)
            enemies_group.update(player, game_map.walls, enemies_group)
            
            hits = pygame.sprite.spritecollide(player, artifacts_group, False)
            for hit in hits:
                score += 10
                save_high_score(score)
                place_object_safely(hit, game_map)

            if pygame.sprite.spritecollideany(player, enemies_group):
                game_state = "game_over"
                save_high_score(score)
                pygame.mixer.music.stop()

            game_map.draw(screen)
            all_sprites.draw(screen)
            draw_ui(screen, score, high_score, game_map.current_level)
            
        elif game_state == "game_over":
            screen.fill((50, 0, 0))
            text = font_end.render("GAME OVER", True, (255, 0, 0))
            sub_text = font_sub.render(f"ESPACE: Rejouer  |  ECHAP: Quitter", True, (255, 255, 255))
            screen.blit(text, (800//2 - text.get_width()//2, 600//2 - 50))
            screen.blit(sub_text, (800//2 - sub_text.get_width()//2, 600//2 + 20))

        elif game_state == "victory":
            screen.fill((0, 50, 0))
            text = font_end.render("VICTOIRE ULTIME !", True, (255, 215, 0))
            sub_text = font_sub.render(f"Tu as vaincu le Boss ! Score: {score}", True, (255, 255, 255))
            screen.blit(text, (800//2 - text.get_width()//2, 600//2 - 50))
            screen.blit(sub_text, (800//2 - sub_text.get_width()//2, 600//2 + 20))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()