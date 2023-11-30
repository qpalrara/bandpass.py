import pygame
from graph import *

class App:
    def __init__(self):
        self.RES = self.WIDTH, self.HEIGHT = 1400, 800
        self.FPS = 60
        self.screen = pygame.display.set_mode(self.RES)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 30)
        self.bp = Graph(self, [0], [0])
       

    def run(self):
        while True:
            self.screen.fill(pygame.Color('white'))
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()

            self.bp.draw()


            pygame.display.set_caption(str(self.clock.get_fps()))
            pygame.display.flip()
            self.clock.tick(self.FPS)

if __name__ == '__main__':
    pygame.init()
    app = App()
    app.run()