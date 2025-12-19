import pygame
from src.models.wall import Wall

class Map:
    def __init__(self):
        # Chargement de la texture du sol
        try:
            self.floor_img = pygame.image.load("assets/images/floor.jpg").convert()
            self.floor_img = pygame.transform.scale(self.floor_img, (64, 64))
        except FileNotFoundError:
            self.floor_img = pygame.Surface((64, 64))
            self.floor_img.fill((34, 139, 34))

        # --- LE PLAN DE TON NIVEAU ---
        # W = Mur (Wall), . = Sol
        self.layout = [
            "WWWWWWWWWWWW",
            "W..........W",
            "W..WW..WW..W",
            "W..........W",
            "W....WW....W",
            "W..........W",
            "W..........W",
            "W...WWWW...W",
            "W..........W",
            "WWWWWWWWWWWW",
        ]
        # -----------------------------
        
        self.walls = pygame.sprite.Group()
        self._generate_walls()

    def _generate_walls(self):
        # On lit le plan lettre par lettre
        for row_index, row in enumerate(self.layout):
            for col_index, letter in enumerate(row):
                x = col_index * 64
                y = row_index * 64
                
                if letter == "W":
                    wall = Wall(x, y)
                    self.walls.add(wall)

    def draw(self, screen):
        for x in range(0, 800, 64):
            for y in range(0, 640, 64):
                screen.blit(self.floor_img, (x, y))
        
        self.walls.draw(screen)