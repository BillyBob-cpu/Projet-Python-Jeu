import pygame
# Importations futures de tes contrôleurs et vues

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Mon Projet Pygame")
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((30, 30, 30)) # Un fond gris foncé
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()