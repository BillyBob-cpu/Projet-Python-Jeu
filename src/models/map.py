import pygame
from src.models.wall import Wall

class Map:
    def __init__(self):
        try:
            self.floor_img = pygame.image.load("assets/images/floor.jpg").convert()
            self.floor_img = pygame.transform.scale(self.floor_img, (64, 64))
        except FileNotFoundError:
            self.floor_img = pygame.Surface((64, 64))
            self.floor_img.fill((34, 139, 34))

        self.walls = pygame.sprite.Group()
        self.current_level = 1
        
        # NIVEAU 1 : Le Visage
        self.level_1 = [
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

        # NIVEAU 2 : Les Piliers
        self.level_2 = [
            "WWWWWWWWWWWW",
            "W..........W",
            "W.WW.WW.WW.W",
            "W..........W",
            "W.WW.WW.WW.W",
            "W..........W",
            "W.WW.WW.WW.W",
            "W..........W",
            "W..........W",
            "WWWWWWWWWWWW",
        ]

        # NIVEAU 3 : TA CARTE PERSONNALISÉE
        self.level_3 = [
            "WWWWWWWWWWWW",
            "W..........W",
            "W....W...W.W",
            "W.W........W", # J'ai ajusté pour que le mur ferme bien à droite
            "W....W.....W", 
            "W.W.....W..W",
            "W...W.W....W",
            "W.......W..W",
            "W..........W",
            "WWWWWWWWWWWW",
        ]
        
        self.load_level(1)

    def load_level(self, level_num):
        self.current_level = level_num
        self.walls.empty()
        
        if level_num == 1:
            layout = self.level_1
        elif level_num == 2:
            layout = self.level_2
        else:
            layout = self.level_3
        
        for row_index, row in enumerate(layout):
            for col_index, letter in enumerate(row):
                if letter == "W":
                    wall = Wall(col_index * 64, row_index * 64)
                    self.walls.add(wall)

    def get_empty_spots(self):
        spots = []
        if self.current_level == 1:
            layout = self.level_1
        elif self.current_level == 2:
            layout = self.level_2
        else:
            layout = self.level_3

        for row_index, row in enumerate(layout):
            for col_index, letter in enumerate(row):
                if letter == ".":
                    spots.append((col_index * 64 + 10, row_index * 64 + 10))
        return spots
        
    def draw(self, screen):
        for x in range(0, 800, 64):
            for y in range(0, 640, 64):
                screen.blit(self.floor_img, (x, y))
        self.walls.draw(screen)