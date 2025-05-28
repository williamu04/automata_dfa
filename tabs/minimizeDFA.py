import streamlit as st
from  helper.inputDFA import input_dfa
from helper.visualizeGraph import render_dfa

def minimize_dfa():
    st.markdown('<div class="logo-container">🔽</div>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; color: #FF6B6B;">DFA Minimization</h2>', unsafe_allow_html=True)
    
    dfa = input_dfa(index=1)

    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📊 Original DFA")
        if dfa:
            st.info(f"States: {len(dfa.states)}")
    
    with col2:
        st.markdown("### ⚡ Actions")
        minimize_button = st.button("🔧 Minimize DFA", type="primary", use_container_width=True)

    if minimize_button and dfa:
        with st.spinner('🔄 Minimizing DFA...'):
            minimized = dfa.minimize()

            st.markdown("## 🎯 Result Comparison")
            vis1 = dfa.get_visual_representation()
            vis2 = minimized.get_visual_representation()

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 🧾 Original DFA")
                st.metric("States", len(dfa.states))
                st.metric("Accept States", len(dfa.accept_states))
                graph1 = render_dfa(vis1)
                if graph1:
                    st.graphviz_chart(graph1)
                else:
                    st.info("Graphviz not available for Original DFA.")

            with col2:
                st.markdown("### ✨ Minimized DFA")
                st.metric("States", len(minimized.states))
                st.metric("Accept States", len(minimized.accept_states))
                graph2 = render_dfa(vis2)
                if graph2:
                    st.graphviz_chart(graph2)
                    st.json({
                    "states": list(minimized.states),
                    "start_state": minimized.start_state,
                    "accept_states": list(minimized.accept_states),
                    "transitions": minimized.transitions
                })
                else:
                    st.info("Graphviz not available for Minimized DFA.")

            st.markdown("---")
            st.markdown("### 📈 Optimization Summary")
            original_states = len(dfa.states)
            minimized_states = len(minimized.states)
            reduction = ((original_states - minimized_states) / original_states * 100) if original_states > 0 else 0

            col1, col2, col3 = st.columns(3)
            col1.metric("Original States", original_states)
            col2.metric("Minimized States", minimized_states)
            col3.metric("Reduction", f"{reduction:.1f}%", f"-{original_states - minimized_states}")
