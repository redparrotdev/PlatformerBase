import pygame
from lib import Assets, Animation, Animator


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.position = pygame.Vector2()
        self.velocity = pygame.Vector2()
        self.acceleration = pygame.Vector2()

        self.dx = 0  # Player horizontal movement direction
        self.speed = 600  # speed in pixel/second
        self.jump_force = -600  # jump force in pixel/second
        self.gravity = self.jump_force * -2 # gravity power

        self.state = "idle"
        self.on_ground = False
        self.facing_left = False

    def load_animations(self):
        self.animator = Animator()
        # Get all animations
        idle_animation = Animation(Assets.get("hero_idle"), 1)
        run_animation = Animation(Assets.get("hero_run"), 1)
        jump_animation = Animation(Assets.get("hero_jump"), 0.45)
        fall_animation = Animation(Assets.get("hero_fall"), 0.45)

        # Add animation to animator
        self.animator.add("idle", idle_animation)
        self.animator.add("run", run_animation)
        self.animator.add("jump", jump_animation)
        self.animator.add("fall", fall_animation)

        # Play the first animation to setup player visual properties
        self.animator.play("run")

        # Setup visual properties
        self.image = self.animator.get_frame()
        self.rect = self.image.get_bounding_rect()

    def __get_state(self, dt):
        if self.velocity.y < 0:
            self.state = "jump"
        elif self.velocity.y > self.gravity * dt:
            self.state = "fall"
        else:
            if self.dx != 0:
                self.state = "run"
            else:
                self.state = "idle"

    def move_x(self, dt):
        self.velocity.x = (self.speed + self.acceleration.x) * dt
        self.position.x += self.velocity.x * self.dx
        self.rect.x = round(self.position.x)

    def move_y(self, dt):
        self.velocity.y += self.gravity * dt
        self.position.y += (self.velocity.y + self.acceleration.y) * dt
        self.rect.y = round(self.position.y)

    def jump(self):
        self.velocity.y = self.jump_force

    def update(self, dt):
        self.__get_state(dt)
        self.animator.play(self.state)
        self.animator.update(dt)

    def render(self, win, offset):
        self.image = self.animator.get_frame()

        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)

        image_rect = self.image.get_rect(midbottom=self.rect.midbottom)

        win.blit(self.image, image_rect.topleft - offset)
