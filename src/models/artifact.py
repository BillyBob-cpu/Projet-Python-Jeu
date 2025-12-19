import pygame

class Artifact(pygame.sprite.Sprite):
    def __init__(self, x, y, is_final_treasure=False):
        super().__init__()
        
        image_name = "pharaon_treasure.png" if is_final_treasure else "artifact.png"
        
        try:
            self.image = pygame.image.load(f"assets/images/{image_name}").convert_alpha()
            size = (60, 60) if is_final_treasure else (40, 40)
            self.image = pygame.transform.scale(self.image, size)
        except FileNotFoundError:
            self.image = pygame.Surface((40, 40))
            self.image.fill((255, 215, 0)) 
            
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)