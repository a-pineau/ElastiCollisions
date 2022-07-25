import os
import random
import pygame as pg
import math

from particle import Particle
from settings import *

vec = pg.math.Vector2
# Manually places the window at coords (x, y)
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100, 100)

class Simulation:
    def __init__(self, n_particles=10, record=False) -> None:
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode([WIDTH, HEIGHT])
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.particles = []
        self.n_particles = n_particles
        self.n_frame = 0
        self.n_collisions = 0
        self.record = record
    
    def new(self):
        # Building a new simulation
        try:
            os.mkdir(SNAP_FOLDER)
        except FileExistsError:
            print(f"Folder \"{SNAP_FOLDER}\" already exists. Ignoring.")
        if os.path.isdir(SNAP_FOLDER):
            for file_name in os.listdir(SNAP_FOLDER):
                file = os.path.join(SNAP_FOLDER, file_name)
                os.remove(file)
                
        # Building random particles
        for _ in range(self.n_particles):
            while True:
                r = random.randint(MIN_RAD, MAX_RAD)
                x, y = random.randint(0 + r, WIDTH-r), random.randint(0 + r, HEIGHT-r)
                v_x, v_y = random.randint(1, MAX_VEL), random.randint(1, MAX_VEL)
                # Lets assume that we're not picking the same color twice
                color = tuple(random.choices(range(256), k=3))
                p = Particle(r, x, y, v_x, v_y, color)
                # Check if the current particle doesn't overlap an existing one
                # Can cause the code to crash if the whole screen gets overlaped (need fix)
                for p2 in self.particles:
                    if p2.overlaps(p):
                        break
                else:
                    self.particles.append(p)
                    break

    def handle_collisions(self):
        # Collisions handler
        for i, p in enumerate(self.particles):
            for other in self.particles[i+1:]:
                if p.overlaps(other): 
                    self.n_collisions += 1
                    self.elastic_collisions(p, other)
                
    def elastic_collisions(self, p1, p2):
        x1, x2 = p1.pos, p2.pos 
        m1, m2 = p1.r**2, p2.r**2
        M = m1 + m2
        R = p1.r + p2.r 
        v1, v2 = p1.vel, p2.vel
        # The distance has already been computed, can simplify here
        d_square = pg.math.Vector2.magnitude_squared(x1 - x2)
        d = math.sqrt(d_square)
        disp = (d - R) * 0.5
        n = vec(x2[0] - x1[0], x2[1] - x1[1])  
        # Computing new velocities
        n_v1 = v1 - 2*m2 / M * pg.math.Vector2.dot(v1 - v2, x1 - x2) * (x1 - x2) / d_square
        n_v2 = v2 - 2*m1 / M * pg.math.Vector2.dot(v2 - v1, x2 - x1) * (x2 - x1) / d_square
        p1.vel = n_v1
        p2.vel = n_v2
        # Dealing with sticky collisions issues
        p1.pos.x += disp * (n.x / d)
        p1.pos.y += disp * (n.y / d)
        p2.pos.x -= disp * (n.x / d)
        p2.pos.y -= disp * (n.y / d)
        
    def run(self):
        # Game loop
        while self.running: 
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.display()
            if self.record: self.save_results()
    
    def update(self):
        # Simulation loop update
        self.n_frame += 1
        for p in self.particles:
            p.update()
        self.handle_collisions() 

    def events(self):
        # Closing simulation
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                    
    def display(self):
        # Simulation display
        self.screen.fill(BACKGROUND)
        self.screen.blit(
            pygame.font.SysFont("Calibri", 35).render(f"Collisions: {self.n_collisions}", 
            True, 
            WHITE), 
            (5, 5))
        for p in self.particles:
            pg.draw.circle(self.screen, p.color, p.pos, p.r)
        pg.display.flip()
    
    def save_results(self, extension="png") -> None:
        file_name = f"snapshot_{self.n_frame}.{extension}"
        pygame.image.save(self.screen, os.path.join(SNAP_FOLDER, file_name))


def main():
    sim = Simulation(n_particles=50, record=True)
    sim.new()
    sim.run()
    pg.quit()

if __name__ == "__main__":
    main()