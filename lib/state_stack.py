

from os import stat


class State:

    is_visible = True

    def update(self, dt):
        pass

    def render(self, win):
        pass 


class StateStack:
    
    __stack = []

    @staticmethod
    def push(state):
        StateStack.__stack.append(state)

    @staticmethod
    def pop(count=1):
        states = []

        for i in range(count):
            if len(StateStack.__stack) > 0:
                states.append(StateStack.__stack.pop())

        if len(states) == 1:
            return states[0]

        return states

    @staticmethod
    def peek():
        if len(StateStack.__stack) > 0:
            return StateStack.__stack[-1]

    @staticmethod
    def update(dt):
        if len(StateStack.__stack) > 0:
            StateStack.__stack[-1].update(dt)

    @staticmethod
    def render(win):
        for state in StateStack.__stack:
            if not state.is_visible:
                continue
            state.render(win)
