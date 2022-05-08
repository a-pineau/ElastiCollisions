import math
import pygame as pg
from settings import *
vec = pg.math.Vector2
        
# --------------------------------------------------------------
# Platform

class Particle(pg.sprite.Sprite):
    def __init__(self, r, x, y, v_x, v_y, color):
        pg.sprite.Sprite.__init__(self)
        self.r = r
        self.m = r**2 * math.pi
        self.pos = vec(x, y)
        self.vel = vec(v_x, v_y)
        self.color = color
        
    def update(self) -> None:
        self.pos += self.vel
        if self.pos.x + self.r > WIDTH:
            self.pos.x = WIDTH - self.r
            self.vel.x *= -1
        if self.pos.x - self.r < 0:
            self.pos.x = self.r
            self.vel.x *= -1
        if self.pos.y + self.r > HEIGHT:
            self.pos.y = HEIGHT - self.r
            self.vel.y *= -1
        if self.pos.y - self.r < 0:
            self.pos.y = self.r
            self.vel.y *= -1
            
    def overlaps(self, other) -> bool:
        return self.pos.distance_to(other.pos) < self.r + other.r
    
def main():
    pass

if __name__ == "__main__":
    main()




