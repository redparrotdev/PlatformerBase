

class Timers:

    class Timer:

        def __init__(self, time, action, repeat=False):
            self.time = time
            self.counter = 0
            self.action = action
            self.repeat = repeat

        def invoke(self):
            if self.action is None:
                return
            
            self.action()

    __timer_id = 0
    __timers = {}
    __timers_to_add = []
    __timers_to_delete = []

    @staticmethod
    def add(time: float, action, repeat=False) -> int:
        tid = Timers.__timer_id
        timer = Timers.Timer(time, action, repeat)
        Timers.__timers_to_add.append((tid, timer))

        Timers.__timer_id += 1

        return tid

    @staticmethod
    def delete(id):
        if id not in Timers.__timers:
            return

        Timers.__timers_to_delete.append(id)

    @staticmethod
    def update(dt):
        for id, timer in Timers.__timers_to_add:
            Timers.__timers[id] = timer

        for id in Timers.__timers_to_delete:
            Timers.__timers.pop(id)

        Timers.__timers_to_add.clear()
        Timers.__timers_to_delete.clear()

        for id, timer in Timers.__timers.items():
            timer.counter += dt

            while timer.counter > timer.time:
                timer.invoke()

                if timer.repeat:
                    timer.counter -= timer.time
                else:
                    Timers.delete(id)
