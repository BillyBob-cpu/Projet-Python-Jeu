import pygame

class Artifact(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            self.image = pygame.image.load("assets/images/artifact.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (40, 40)) 
        except FileNotFoundError:
            self.image = pygame.Surface((40, 40))
            self.image.fill((255, 215, 0)) 
            
        self.rect = self.image.get_rect()
        self.rect.center = (x, y) 