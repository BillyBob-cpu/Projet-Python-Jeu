import pygame
import sys
from src.models.player import Player
from src.models.map import Map

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Archéologie & Enigmes")
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    
    player = Player(400, 300) 
    
    all_sprites.add(player)

    game_map = Map()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.update(game_map.walls)

        game_map.draw(screen)  
        all_sprites.draw(screen) 
        
        pygame.display.flip()
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()