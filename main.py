import pygame, time
from pygame.locals import *

class Entity:
    def __init__(self, path, loc = (0, 0)):
        """
        Represents an entity
        :param path: The image to represent the entity
        :param loc: THe initial position
        """
        self.image = pygame.image.load(path).convert_alpha()
        self.x, self.y = loc    # The current position
        self.xvel = self.yvel = self.xacc = self.yacc = 0   # The velocity and acceleration vectors
        self.angle = self.rotate = 0    # Thr current angle, and the rotational velocity
        self.width, self.height = self.image.get_size() # Size of the image
        self.radius = min(self.width, self.height) / 1.4 # Fudge factor (square root of 2)
        self.radius_squared = self.radius * self.radius # So we can compare without doing square root


    def draw(self, display):
        """
        Draw the entity
        :param display:
        :return: None
        """
        if self.angle:
            rotated = pygame.transform.rotate(self.image, self.angle)
            xadd = (self.width - rotated.get_width()) / 2
            yadd = (self.height - rotated.get_height()) / 2
        else:
            rotated = self.image
            xadd = yadd = 0

        display.blit(rotated, (self.x + xadd, self.y + yadd))

    def update(self):
        """
        Update the position of the entity
        :return: None
        """
        self.x += self.xvel
        self.y += self.yvel
        self.xvel += self.xacc
        self.yvel += self.yacc
        self.angle += self.rotate
        self.angle %= 360

class Ship(Entity):

    def __init__(self, path, loc=(0,0)):
        super().__init__(path, loc)
        self.rotate = 1

    def update(self, keys):
        super().update()

class Game:
    def __init__(self):
        self.keys = {}
        self.running = True
        self.display = None
        self.size = self.weight, self.height = 800, 600
        self.rate = 50  # 50 ms per frame (20 FPS)

    def start(self):
        pygame.init()
        self.display = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.ship = Ship("ship.png", (200, 200))
        self.running = True
        return self.display is not None

    def is_pressed(self, key):
        return self.keys.get(key)

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.keys[event.key] = True
            if event.key == pygame.K_ESCAPE:
                self.running = False
        elif event.type == pygame.KEYUP:
            self.keys[event.key] = False
        elif event.type == pygame.QUIT:
            self.running = False

    def update(self):
        self.ship.update(self.keys)

    def render(self):
        display = pygame.display.get_surface()
        self.ship.draw(display)
        pygame.draw
        pygame.display.flip()

    def finish(self):
        pygame.quit()

    def run(self):
        self.running = self.start()

        last_time = time.time() * 1000
        while (self.running):
            for event in pygame.event.get():
                self.on_event(event)
            current_time = time.time() * 1000
            elapsed_time = current_time - last_time
            last_time = current_time
            self.update()
            self.render()
            delay = max(1, self.rate - elapsed_time)
            time.sleep(delay / 1000)
        self.finish()


if __name__ == "__main__":
    game = Game()
    game.run()