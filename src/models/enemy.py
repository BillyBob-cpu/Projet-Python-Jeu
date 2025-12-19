import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            self.image = pygame.image.load("assets/images/enemy.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 50))
        except FileNotFoundError:
            self.image = pygame.Surface((50, 50))
            self.image.fill((148, 0, 211)) 
            
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 2 # Tu peux baisser à 1 si c'est trop dur !

    def update(self, player, walls):
        """
        Déplacement intelligent : va vers le joueur
        """
        dx, dy = 0, 0
        
        # --- 1. Calcul de la direction vers le joueur ---
        # Est-ce que le joueur est à gauche ou à droite ?
        if player.rect.x > self.rect.x:
            dx = self.speed
        elif player.rect.x < self.rect.x:
            dx = -self.speed
            
        # Est-ce que le joueur est en haut ou en bas ?
        if player.rect.y > self.rect.y:
            dy = self.speed
        elif player.rect.y < self.rect.y:
            dy = -self.speed

        # --- 2. Mouvement et Collisions (Pour ne pas traverser les murs) ---
        
        # Mouvement X
        self.rect.x += dx
        if pygame.sprite.spritecollideany(self, walls):
            self.rect.x -= dx # Si on tape un mur, on annule le mouvement X

        # Mouvement Y
        self.rect.y += dy
        if pygame.sprite.spritecollideany(self, walls):
            self.rect.y -= dy # Si on tape un mur, on annule le mouvement Y