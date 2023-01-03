from common import Directions
# state, transition and state machine
class State:
    def __init__(self, name) -> None:
        self.name = name

    def enter(self):
        pass

    def update(self):
        pass

    def exit(self):
        pass
    
class Transition:
    def __init__(self, _from, _to) -> None:
        self._from = _from
        self._to = _to

class FSM:
    def __init__(self, states: list[State], transitions: dict[Transition]) -> None:
        self._states = states
        self._transitions = transitions

        self.current: State = self._states[0]
        self.end: State = self._states[-1]
        
    def get_cstate(self):
        return self.current

    def update(self, event, object, dir=Directions.RIGHT):
        if event:
            if self._transitions.get(event)==None:
                print(self._transitions)
            for trans in self._transitions.get(event):
                if trans._from == self.current:
                    self.current.exit(object)
                    self.current = trans._to
                    self.current.enter(object)
        
        self.current.update(self.current,object=object,dir=dir)
        
        if self.current == self.end:
            self.current.exit(object)
            return False
        return True
