from state_machine import State, CompositeState, FinalState, StateMachine, PseudoState
import pygraphviz as pgv
from IPython.display import SVG, display

initial_style= {
    'shape': 'circle',
    'width': '0.2',
    'style': 'filled',
    'fillcolor': 'black',
    'color': 'black',
}

final_style= {
    'shape': 'doublecircle',
    'width': '0.2',
    'style': 'filled',
    'fillcolor': 'black',
    'color': 'black',
}


def state_with_most_outbound_transitions(machine):
    mx=0
    r=None
    for s in machine.states.values():
        if isinstance( s, State):
            l = len(s.transitions)
            if l>mx:
                mx=l
                r=s
    return r

initial_style= {
    'shape': 'circle',
    'width': '0.2',
    'style': 'filled',
    'fillcolor': 'black',
    'color': 'black',
}

final_style= {
    'shape': 'doublecircle',
    'width': '0.2',
    'style': 'filled',
    'fillcolor': 'black',
    'color': 'black',
}

def draw_nodes(machine, graph):

    initial_node = 'initial_%s'%machine.name
    graph.add_node(initial_node, label='', **initial_style)
    target = machine.initial_state
    if type(target)==State:
        target_name = target.name
        graph.add_edge( initial_node, target_name, label='start')
    elif type(target)==CompositeState:
        lhead = 'cluster_%s'%target.name
        target_state = state_with_most_outbound_transitions(target)
        target_name  = target_state.name
        graph.add_edge( initial_node, target_name, lhead=lhead, label='start' )
    elif type(target)==PseudoState:
        target_name = target.name
        graph.add_edge( initial_node, target_name, label='start')
    elif target is None:
        raise Exception( 'Initial State Not Set')
    else:
        raise NotImplementedError('Not implemented for target type %s'%type(target))

    for k, s in machine.states.items():
        if type(s)==State:
            graph.add_node( s.name )
        elif type(s)==CompositeState:
            print('Drawing %s as a composite'%s.name)
            cluster_name = 'cluster_%s'%s.name
            sub = graph.add_subgraph(name=cluster_name, label=s.name)#, rank='same')
            draw_nodes(s, sub)
        elif type(s)==FinalState:
            graph.add_node( s.name, label='', **final_style )
        elif type(s)==PseudoState:
            graph.add_node( s.name, shape='diamond' )
        elif s is None:
            raise Exception('State is None. Did you forget to set the initial state?')
        else:
            raise NotImplementedError('Not implemented for %s'%type(s))


def draw_transitions( machine, graph ):
    for k, s in machine.states.items():
        draw_state_transitions( s, graph )

        if isinstance(s, StateMachine):
            draw_transitions(s, graph)


def draw_state_transitions( state, graph ):
    ltail = None
    source_state = None
    if type(state)==State:
        source_state = state
    elif type(state)==CompositeState:
        source_state = state_with_most_outbound_transitions( state )
        ltail = 'cluster_%s'%state.name
        print( 'tail for %s is %s'%(state,ltail))
    elif type(state)==PseudoState:
        source_state=state

    for t in state.transitions:
        target = t.target
        if type(target) in (State, FinalState):
            lhead = None
            target_name = t.target.name
        elif type(target)==CompositeState:
            lhead = 'cluster_%s'%target.name
            target_state = target.initial_state
            target_name  = target_state.name
        else:
            raise NotImplemented()
        #print('Adding edge from %s to %s, ltail=%s'%(source_state.name, target_name, ltail))
        kwargs = {'label':t.to_str()}
        if ltail: kwargs['ltail']=ltail
        if lhead: kwargs['lhead']=lhead

        graph.add_edge( source_state.name, target_name, **kwargs )

def draw_machine(machine, filename=None):
    filename=filename or 'state.svg'
    G = pgv.AGraph(compound=True,directed=True)
    draw_nodes( machine, G )
    draw_transitions( machine, G )
    return G

def display_machine(machine, filename=None):
    filename = filename or 'state.svg'
    G = draw_machine(machine)
    G.draw(filename, prog='dot')
    display(SVG(filename))
