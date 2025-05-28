import streamlit as st
from helper.inputDFA import input_dfa
from helper.visualizeGraph import render_dfa
from helper.visualizeTable import render_table 


# ===================== TAB FUNCTIONS =====================
def simulate_dfa():
    st.markdown('<div class="logo-container">🔁</div>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; color: #4ECDC4;">DFA String Testing</h2>', unsafe_allow_html=True)
    
    dfa = input_dfa(index=1)
    
    st.markdown("---")
    st.markdown("### 🧪 Test Your String")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        test_string = st.text_input("🔤 Enter string to test", "", placeholder="Enter your test string here...")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        test_button = st.button("🚀 Run Simulation", type="primary", use_container_width=True)
    
    if dfa:
        # Visualize the DFA structure
        st.markdown("---")
        st.markdown("### 🔍 **DFA Structure Visualization**")
        
        # Get DFA visual representation
        dfa_visual = dfa.get_visual_representation()
        
        # Display DFA statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total States", dfa_visual["num_states"])
        with col2:
            st.metric("Accept States", len(dfa_visual["accept_states"]))
        with col3:
            st.metric("Complete DFA", "Yes" if dfa_visual["is_complete"] else "No")
        
        # Display DFA details
        with st.expander("🔄 **DFA State Diagram**", expanded=True):
            # Visual graph representation
            st.markdown("#### State Diagram (Graph)")
            graph = render_dfa(dfa_visual)
            if graph:
                st.graphviz_chart(graph)
            else:
                st.info("🖼️ Graph visualization requires Graphviz package. Please install with `pip install graphviz` and ensure Graphviz software is installed.")
            
            # Display transition table
            st.markdown("#### Transition Table")
            render_table(dfa_visual)
    
    if test_button and dfa and test_string is not None:
        with st.spinner('🔄 Running DFA simulation...'):
            result = dfa.simulate(test_string)
            if result:
                st.balloons()
                st.success(f"🎉 **ACCEPTED!** String '{test_string}' is accepted by the DFA")
            else:
                st.error(f"❌ **REJECTED!** String '{test_string}' is not accepted by the DFA")

