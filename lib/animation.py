

class Animation:
    
    def __init__(self, frames, duration, repeat=True):
        self.frames = frames
        self.duration = duration
        self.repeat = repeat
        self.frames_count = len(self.frames)
        self.frame_time = self.duration / self.frames_count

        # Handlers
        self.on_animation_end = None

    def animation_end(self):
        if self.on_animation_end is None:
            return

        self.on_animation_end.invoke()


class Animator:
    
    def __init__(self):
        self.__animations = {}
        self.time = 0
        self.index = 0
        self.current_animation_name = None

    def add(self, name, animation):
        self.__animations[name] = animation

    def play(self, name):
        if self.current_animation_name == name:
            return False

        self.time = 0
        self.index = 0
        self.current_animation_name = name
        return True

    def update(self, dt):
        if self.current_animation_name is None:
            return

        animation = self.__animations[self.current_animation_name]

        if animation.frames_count == 1:
            return

        self.time += dt

        while self.time > animation.frame_time:
            self.index += 1

            if self.index == animation.frames_count:
                if animation.repeat:
                    self.index = 0
                else:
                    self.index = animation.frames_count - 1

                animation.animation_end()

            self.time -= animation.frame_time

    def get_frame(self):
        return self.__animations[self.current_animation_name].frames[self.index]
