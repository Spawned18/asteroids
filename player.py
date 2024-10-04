# type: ignore
import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y, updatable_group, drawable_group):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        updatable_group.add(self)
        drawable_group.add(self)
        self.rect = pygame.Rect(x - PLAYER_RADIUS, y - PLAYER_RADIUS, PLAYER_RADIUS * 2, PLAYER_RADIUS * 2)
        self.image = pygame.Surface((PLAYER_RADIUS * 2, PLAYER_RADIUS * 2), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))  # Transparent
        pygame.draw.polygon(self.image, "white", self.triangle(), 2)
        
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = forward.rotate(90)
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right * self.radius / 2
        c = self.position - forward * self.radius + right * self.radius / 2
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(
        screen,
        "white",
        self.triangle(),
        2
    )
    
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
    
    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt) # rotate left
        if keys[pygame.K_d]:
            self.rotate(dt) # rotate right
        if keys[pygame.K_s]:
            self.move(-dt) # move backwards
        if keys[pygame.K_w]:
            self.move(dt) # move forwards
        if keys[pygame.K_SPACE]:
            self.shoot() # shoot

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
        self.rect.center = self.position

    def shoot(self):
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED