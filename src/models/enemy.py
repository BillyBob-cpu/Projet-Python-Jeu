import pygame
import math

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, is_boss=False):
        super().__init__()
        self.is_boss = is_boss
        
        if self.is_boss:
            try:
                self.image = pygame.image.load("assets/images/boss.png").convert_alpha()
                self.image = pygame.transform.scale(self.image, (60, 60))
            except FileNotFoundError:
                self.image = pygame.Surface((60, 60))
                self.image.fill((255, 0, 0)) 
            
            self.speed = 3 
        else:
            try:
                self.image = pygame.image.load("assets/images/enemy.png").convert_alpha()
                self.image = pygame.transform.scale(self.image, (50, 50))
            except FileNotFoundError:
                self.image = pygame.Surface((50, 50))
                self.image.fill((148, 0, 211))
            self.speed = 2

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self, player, walls, enemies_group):
        """
        Gère le déplacement et les collisions (Murs + Autres ennemis)
        """
        dx, dy = 0, 0
        
        if player.rect.x > self.rect.x:
            dx = self.speed
        elif player.rect.x < self.rect.x:
            dx = -self.speed
            
        if player.rect.y > self.rect.y:
            dy = self.speed
        elif player.rect.y < self.rect.y:
            dy = -self.speed

        self.rect.x += dx
        
        hit_wall = pygame.sprite.spritecollideany(self, walls)
        if hit_wall:
            if self.is_boss: 
                 if dx > 0: self.rect.right = hit_wall.rect.left
                 if dx < 0: self.rect.left = hit_wall.rect.right
            else:
                self.rect.x -= dx 

        hit_enemies = pygame.sprite.spritecollide(self, enemies_group, False)
        for other in hit_enemies:
            if other != self: 
                self.rect.x -= dx 

        self.rect.y += dy
        
        hit_wall = pygame.sprite.spritecollideany(self, walls)
        if hit_wall:
            if self.is_boss:
                if dy > 0: self.rect.bottom = hit_wall.rect.top
                if dy < 0: self.rect.top = hit_wall.rect.bottom
            else:
                self.rect.y -= dy

        hit_enemies = pygame.sprite.spritecollide(self, enemies_group, False)
        for other in hit_enemies:
            if other != self:
                self.rect.y -= dy