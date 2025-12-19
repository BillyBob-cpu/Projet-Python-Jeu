import pygame
import sys
from src.models.player import Player
from src.models.map import Map
from src.models.artifact import Artifact

def draw_ui(screen, score):
    # Choisir une police d'écriture (None = police par défaut, 36 = taille)
    font = pygame.font.Font(None, 36)
    # Créer l'image du texte (Texte, Antialising, Couleur)
    text_surface = font.render(f"Score: {score}", True, (255, 255, 255))
    # Afficher en haut à gauche (10, 10)
    screen.blit(text_surface, (10, 10))

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Archéologie & Enigmes")
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    
    player = Player(400, 300) 

    artifacts_group = pygame.sprite.Group()
    
    treasure = Artifact(600, 150)
    artifacts_group.add(treasure)
    all_sprites.add(treasure) 
    
    score = 0
    
    all_sprites.add(player)

    game_map = Map()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.update(game_map.walls)

        hits = pygame.sprite.spritecollide(player, artifacts_group, True)
        
        for hit in hits:
            score += 10
            print(f"Trésor trouvé ! Score actuel : {score}")

        game_map.draw(screen)  
        all_sprites.draw(screen) 

        draw_ui(screen, score) 
        
        
        pygame.display.flip()
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()