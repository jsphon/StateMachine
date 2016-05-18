
from state_machine.transition import Transition, DefaultTransition
from collections import defaultdict

class BaseState( object ):

    def __init__(self, name, machine):
        self.name=name
        self.machine=machine
        self.default_transition=None

        self.start_event = None

        self.on_start = None
        self.on_end = None
        self.on_run = None
        self._vars = {}

        self._logger = None

    def __repr__(self):
        return 'State:%s'%self.name

    @property
    def vars(self):
        return self._vars

    @property
    def logger(self):
        return self._logger or self.machine.logger

    @logger.setter
    def logger(self, value):
        self._logger = value

    def notify_observers(self, event):
        self.machine.notify_observers(event)

    def add_default_transition_to(self, target):
        self.default_transition = DefaultTransition(target)

    def add_transition_to(self, target, trigger=None, guard=None, action=None):
        pass

    def start(self, event):
        #self.logger.info( 'Starting state %s', self.name )
        self._vars.clear()
        self.start_event=event
        if self.on_start:
            self.on_start(event,self)

    def end(self, event):
        #self.logger.info( 'Ending state %s', self.name )
        if self.on_end:
            self.on_end(event, self)
        self._vars.clear()

    def run(self, event):
        if self.on_run:
            self.on_run(event, self)

    def next_transition(self, event):
        pass


class State(BaseState):

    def __init__(self, name, machine):
        super(State, self).__init__(name, machine)
        self.listeners = defaultdict(list)

    def __repr__(self):
        return 'State:%s'%self.name

    def add_transition_to(self, target, trigger=None, guard=None, action=None):
        t = Transition(self, target, trigger=trigger, guard=guard, action=action)
        if trigger:
            self.listeners[trigger].append(t)
        elif self.default_transition:
            raise Exception('Default transition already exists')
        else:
            self.default_transition=t

    def next_transition(self, event):
        transitions = self.listeners[event.name]
        for t in transitions:
            if t.is_triggered(event):
                return t
        return self.default_transition


class PseudoState(BaseState):
    """ This tests for transitions immediately  and does not listen to events
    """

    def __init__(self, name, machine):
        super(PseudoState, self).__init__(name, machine)
        self.transitions = []

    def add_transition_to(self, target, trigger=None, guard=None, action=None):
        assert trigger is None, 'triggers should be None in PseudoStates'
        t = Transition(self, target, trigger=trigger, guard=guard, action=action)
        self.transitions.append(t)

    def next_transition(self, event):
        for t in self.transitions:
            if t.is_triggered(event):
                return t


class FinalState(object):
    name='Final State'