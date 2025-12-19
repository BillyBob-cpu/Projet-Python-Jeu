import pygame

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            self.image = pygame.image.load("assets/images/wall.jpg").convert()
            self.image = pygame.transform.scale(self.image, (64, 64))
        except FileNotFoundError:
            self.image = pygame.Surface((64, 64))
            self.image.fill((100, 100, 100)) 
            
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)