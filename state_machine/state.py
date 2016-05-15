
from state_machine.transition import Transition, DefaultTransition
from collections import defaultdict

class BaseState( object ):

    start_event = None

    on_start = None
    on_end = None

    def __init__(self, name, machine):
        self.name=name
        self.machine=machine
        self.default_transition=None
        self.vars = {}

    def __repr__(self):
        return 'State:%s'%self.name

    @property
    def logger(self):
        return self.machine.logger

    def notify_observers(self, event):
        self.machine.notify_observers(event)

    def add_default_transition_to(self, target):
        """
        Add a default transition to target
        :param target:  the target state
        :return:
        """
        self.default_transition = DefaultTransition(target)

    def add_transition_to(self, target, trigger=None, guard=None, action=None):
        pass

    def start(self, event):
        self.start_event=event
        if self.on_start:
            self.on_start(event,self)

    def end(self, event):
        self.vars = {}
        if self.on_end:
            self.on_end(event, self)

    def run(self, event):
        """
        For doing something everytime the machine ticks, such as storing state
        """
        pass

    def next_transition(self, event):
        pass


class State(BaseState):

    start_event = None

    def __init__(self, name, machine):
        super(State, self).__init__(name, machine)
        self.listeners = defaultdict(list)
        self.default_transition=None
        self.vars = {}

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
            #model.logger.info('Testing transition %s',t)
            if t.is_triggered(event):
                #model.logger.info( 'Returning %s',t)
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


class FinalState(State):

    def __init__(self, name=None):
        name = name or 'Final State'
        super(FinalState, self).__init__(name)

    def find_next_triggered_transition(self, data, model):
        """ This does nothing """
        pass