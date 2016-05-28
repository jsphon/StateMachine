
from state_machine.transition import Transition, DefaultTransition
from collections import defaultdict

class BaseState( object ):

    def __init__(self, name, machine):
        self.name=name
        self.machine=machine
        self.default_transition=None

        self.start_event = None

        #  Do we need to refactor this, as Final States do not have on_end or vars
        # PseudoState might not have on_run, as they exit straight away.
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
        self.default_transition = DefaultTransition(self, target)

    def add_transition_to(self, target, trigger=None, guard=None, action=None):
        pass

    def start(self, event):
        #self.logger.info( 'Starting state %s', self.name )
        #self._vars.clear()
        self.start_event=event
        if self.on_start:
            self.on_start(event,self)

    def end(self, event):
        #self.logger.info( 'Ending state %s', self.name )
        if self.on_end:
            self.on_end(event, self)
        #self._vars.clear()

    def run(self, event):
        if self.on_run:
            self.on_run(event, self)

    def next_transition(self, event):
        pass

    @property
    def transitions(self):
        raise NotImplemented()


class State(BaseState):

    def __init__(self, name, machine):
        super(State, self).__init__(name, machine)
        self.transitions_by_trigger = defaultdict(list)

    def __repr__(self):
        return 'State:%s'%self.name

    def add_transition_to(self, target, trigger=None, guard=None, action=None):
        t = Transition(self, target, trigger=trigger, guard=guard, action=action)
        if trigger:
            self.transitions_by_trigger[trigger].append(t)
        elif self.default_transition:
            raise Exception('Default transition already exists')
        else:
            self.default_transition=t

    def next_transition(self, event):
        transitions = self.transitions_by_trigger[event.name]
        for t in transitions:
            if t.is_triggered(event):
                return t
        return self.default_transition

    @property
    def transitions(self):
        result = []
        for transitions in self.transitions_by_trigger.values():
            result.extend(transitions)
        return result


class PseudoState(BaseState):
    """ This tests for transitions immediately  and does not listen to events
    """

    def __init__(self, name, machine):
        super(PseudoState, self).__init__(name, machine)
        self._transitions = []

    def add_transition_to(self, target, trigger=None, guard=None, action=None):
        assert trigger is None, 'triggers should be None in PseudoStates'
        t = Transition(self, target, trigger=trigger, guard=guard, action=action)
        self._transitions.append(t)

    def next_transition(self, event):
        for t in self._transitions:
            if t.is_triggered(event):
                return t
        return self.default_transition

    @property
    def transitions(self):
        if self.default_transition:
            return self._transitions + [ self.default_transition ]
        else:
            return self._transitions

class FinalState(BaseState):

    name='Final State'

    def __init__(self,name='final', machine=None):
        super(FinalState, self).__init__(name, machine)

    @property
    def transitions(self):
        return []