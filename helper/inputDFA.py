import streamlit as st
import json
from engines.DFA import DFA

# ===================== DFA INPUT FUNCTIONS =====================
def input_dfa(index=1):
    st.markdown(f"""
    <div class="feature-card">
        <h3>⚙️ DFA Configuration #{index}</h3>
        <p>Configure your Deterministic Finite Automaton below</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        states = st.text_input(f"🔘 States (comma-separated)", "q0,q1", key=f"states_{index}")
        alphabet = st.text_input(f"🔤 Alphabet (comma-separated)", "a,b", key=f"alphabet_{index}")
    
    with col2:
        start_state = st.text_input(f"▶️ Start State", "q0", key=f"start_{index}")
        accept_states = st.text_input(f"✅ Accept States (comma-separated)", "q1", key=f"accept_{index}")
    
    st.markdown("**🔄 Transition Function (JSON format):**")
    transitions_json = st.text_area(
        f"Define transitions for DFA {index}", 
        '{\n  "q0": {"a": "q1", "b": "q0"},\n  "q1": {"a": "q1", "b": "q0"}\n}',
        height=150,
        key=f"transitions_{index}"
    )
    
    try:
        transitions = json.loads(transitions_json)
        dfa = DFA(
            states=[s.strip() for s in states.split(",")],
            alphabet=[s.strip() for s in alphabet.split(",")],
            start_state=start_state.strip(),
            accept_states=[s.strip() for s in accept_states.split(",")],
            transitions=transitions
        )
        st.success(f"✅ DFA {index} configured successfully!")
        return dfa
    except Exception as e:
        st.error(f"❌ Error parsing DFA {index}: {e}")
        return None