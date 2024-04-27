import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, controls):
        super().__init__()
        self.image = pygame.Surface([50, 50])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.controls = controls

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[self.controls['up']]:
            self.rect.y -= 5
        if keys[self.controls['down']]:
            self.rect.y += 5
        if keys[self.controls['left']]:
            self.rect.x -= 5
        if keys[self.controls['right']]:
            self.rect.x += 5
