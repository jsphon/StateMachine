

from state_machine.exception import StateMachineException
from state_machine.transition import Transition, DefaultTransition
from collections import defaultdict

class State( object ):

    def __init__(self, name, machine):
        self.name=name
        self.machine=machine
        self.listeners = defaultdict(list)
        self.default_transition=None

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

    def add_transition_to(self, target, condition):
        """
        :param target: A State
        :param condition: A condition
        """
        t = Transition(target, condition)
        self.listeners[condition.listens_for].append(t)

    def start(self, event):
        return self.on_start(event)

    def on_start(self, event):
        """ child classes can optionally extend this """
        pass

    def end(self, event):
        self.on_end( event)

    def on_end(self, event ):
        """ child classes can optionally extend this """
        pass

    def run(self, event):
        """
        For doing something everytime the machine ticks, such as storing state
        """
        pass

    def find_next_triggered_transition(self, data, model ):
        """
        Deprecated to next_transition
        """
        raise DeprecationWarning()
        raise NotImplementedError()

    def next_transition(self, event):

        transitions = self.listeners[event.name]
        for t in transitions:
            #model.logger.info('Testing transition %s',t)
            if t.is_triggered(event):
                #model.logger.info( 'Returning %s',t)
                return t

        return self.default_transition

    def notify_observers(self, event):
        '''
        Notify the parent machine's observers
        '''
        self.machine.notify_observers(event)

class FinalState(State):

    def __init__(self, name=None):
        name = name or 'Final State'
        super(FinalState, self).__init__(name)

    def find_next_triggered_transition(self, data, model):
        """ This does nothing """
        pass