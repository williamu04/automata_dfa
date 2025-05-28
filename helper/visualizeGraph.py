import streamlit as st
import graphviz

def render_dfa(dfa_visual):
    """
    Render DFA graph using Streamlit's graphviz_chart.
    
    Args:
        dfa_visual: Visual representation of DFA from get_visual_representation()
        
    Displays:
        A rendered graphviz chart in the Streamlit app.
    """
    dot = graphviz.Digraph()
    dot.attr(rankdir='LR')

    # Add states
    for state in dfa_visual["states"]:
        shape = 'doublecircle' if state in dfa_visual["accept_states"] else 'circle'
        dot.node(state, shape=shape)
    
    # Add invisible start arrow
    dot.node('start', shape='none', label='')
    dot.edge('start', dfa_visual["start_state"])

    # Add transitions
    for src, edges in dfa_visual["transitions"].items():
        for symbol, dest in edges.items():
            dot.edge(src, dest, label=symbol)

    # Display using Streamlit
    st.graphviz_chart(dot)


def render_nfa(nfa_visual):
    """
    Render NFA graph using Streamlit's graphviz_chart.
    
    Args:
        nfa_visual: Visual representation of NFA from get_visual_representation()
        
    Displays:
        A rendered graphviz chart in the Streamlit app.
    """
    dot = graphviz.Digraph()
    dot.attr(rankdir='LR')

    # Add states
    for state in nfa_visual["states"]:
        shape = 'doublecircle' if state in nfa_visual["accept_states"] else 'circle'
        dot.node(state, shape=shape)

    # Add invisible start arrow
    dot.node('start', shape='none', label='')
    dot.edge('start', nfa_visual["start_state"])

    # Add transitions
    for src, transitions in nfa_visual["transitions"].items():
        for symbol, dests in transitions.items():
            symbol_display = 'ε' if symbol == "" else symbol
            for dest in dests:
                dot.edge(src, dest, label=symbol_display)

    # Display using Streamlit
    st.graphviz_chart(dot)
