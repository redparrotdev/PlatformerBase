import pygame
from lib import StateStack, Input, Timers, Assets
from states import PlayState
from settings import Settings


class Game:
    def __init__(self):
        pygame.init()

        self.win = pygame.display.set_mode(Settings.WINDOW_SIZE)
        self.running = True
        self.fill_color = pygame.Color(52, 219, 235)

        pygame.display.set_caption(Settings.GAME_NAME)

        self.clock = pygame.time.Clock()
        self.fps = 60

    def initialize(self):
        self.load_assets()

        Input.initialize()

        ps = PlayState()
        StateStack.push(ps)

    def update(self, dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        Timers.update(dt)
        Input.update()
        StateStack.update(dt)

    def render(self):
        self.win.fill(self.fill_color)

        StateStack.render(self.win)

        pygame.display.flip()

    def run(self):
        self.initialize()

        while self.running:
            dt = self.clock.tick(self.fps) / 1000
            self.update(dt)
            self.render()

        pygame.quit()

    def load_assets(self):
        """
        Load all game content here
        """
        Assets.load_sound("coin_collect", "sounds/coin_collect.wav")

        # Hero animations
        hero_sprite_scale = 1.5

        Assets.load_animation("hero_idle", "hero/_Idle.png", 0, 10, (120, 80), resize=hero_sprite_scale)
        Assets.load_animation("hero_run", "hero/_Run.png", 0, 10, (120, 80), resize=hero_sprite_scale)
        Assets.load_animation("hero_jump", "hero/_Jump.png", 0, 3, (120, 80), resize=hero_sprite_scale)
        Assets.load_animation("hero_fall", "hero/_Fall.png", 0, 3, (120, 80), resize=hero_sprite_scale)


if __name__ == "__main__":
    Game().run()
