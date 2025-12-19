import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Image fixe
        try:
            self.image = pygame.image.load("assets/images/player.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 50)) # Un peu plus petit pour passer les portes
        except FileNotFoundError:
            self.image = pygame.Surface((50, 50))
            self.image.fill((255, 0, 0))
            
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 5

    def update(self, walls):
        """Déplacement avec gestion des collisions"""
        keys = pygame.key.get_pressed()
        
        dx = 0
        dy = 0
        
        # Calcul de la vitesse voulue
        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            dx = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.speed
        if keys[pygame.K_UP] or keys[pygame.K_z]:
            dy = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = self.speed

        self.rect.x += dx
        hits = pygame.sprite.spritecollide(self, walls, False)
        for wall in hits:
            if dx > 0: 
                self.rect.right = wall.rect.left
            if dx < 0: 
                self.rect.left = wall.rect.right

        self.rect.y += dy
        hits = pygame.sprite.spritecollide(self, walls, False)
        for wall in hits:
            if dy > 0: 
                self.rect.bottom = wall.rect.top
            if dy < 0: 
                self.rect.top = wall.rect.bottom