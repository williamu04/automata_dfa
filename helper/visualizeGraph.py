import graphviz
HAS_GRAPHVIZ = True

def render_dfa(dfa_visual):
    """
    Generate a graphviz visualization of DFA structure
    
    Args:
        dfa_visual: Visual representation of DFA from get_visual_representation()
        
    Returns:
        graphviz.Digraph: Graph visualization of the DFA, or None if graphviz not available
    """
    if not HAS_GRAPHVIZ:
        return None
        
    # Create a new directed graph
    graph = graphviz.Digraph()
    graph.attr(rankdir='LR')  # Left to right layout
    
    # Add states (nodes)
    for state in dfa_visual["states"]:
        if state in dfa_visual["accept_states"]:
            # Double circle for accept states
            graph.node(state, shape='doublecircle')
        else:
            # Single circle for non-accept states
            graph.node(state, shape='circle')
    
    # Add a special node for the start state indicator
    graph.node('start', shape='none', label='')
    graph.edge('start', dfa_visual["start_state"])
    
    # Add transitions (edges)
    for src in dfa_visual["transitions"]:
        for symbol, dest in dfa_visual["transitions"][src].items():
            graph.edge(src, dest, label=symbol)
    
    return graph


# ===================== HELPER FUNCTIONS =====================
def render_nfa(nfa_visual):
    """
    Generate a graphviz visualization of NFA structure
    
    Args:
        nfa_visual: Visual representation of NFA from get_visual_representation()
        
    Returns:
        graphviz.Digraph: Graph visualization of the NFA, or None if graphviz not available
    """
    if not HAS_GRAPHVIZ:
        return None
        
    # Create a new directed graph
    graph = graphviz.Digraph()
    graph.attr(rankdir='LR')  # Left to right layout
    
    # Add states (nodes)
    for state in nfa_visual["states"]:
        if state in nfa_visual["accept_states"]:
            # Double circle for accept states
            graph.node(state, shape='doublecircle')
        else:
            # Single circle for non-accept states
            graph.node(state, shape='circle')
    
    # Add a special node for the start state indicator
    graph.node('start', shape='none', label='')
    graph.edge('start', nfa_visual["start_state"])
    
    # Add transitions (edges)
    for src in nfa_visual["transitions"]:
        for symbol, destinations in nfa_visual["transitions"][src].items():
            symbol_display = 'ε' if symbol == "" else symbol
            for dest in destinations:
                graph.edge(src, dest, label=symbol_display)
    
    return graph
