import streamlit as st
from engines.REGEX import regex_to_nfa
from helper.visualizeGraph import render_nfa

def simulate_nfa():
    st.markdown('<div class="logo-container">🔤</div>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; color: #96CEB4;">Regex to NFA Conversion</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="bg-blue-500 mt-5 p-3">
        <h4>📝 Supported Regex Operations:</h4>
        <ul>
            <li><strong>a, b</strong> - Basic symbols</li>
            <li><strong>|</strong> - Union (OR operation)</li>
            <li><strong>*</strong> - Kleene star (zero or more)</li>
            <li><strong>()</strong> - Grouping</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        regex = st.text_input("🎯 Enter Regular Expression", "a(b|a)*", placeholder="Example: a(b|a)*")
        test_string = st.text_input("🧪 Enter test string", "", placeholder="Enter string to test against regex")
    
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        convert_button = st.button("🔄 Convert & Test", type="primary", use_container_width=True)

    if convert_button and regex:
        try:
            with st.spinner('🔄 Converting regex to NFA and testing...'):
                nfa = regex_to_nfa(regex)
                result = nfa.simulate(test_string)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("### ✅ **Conversion Successful!**")
                    st.success(f"Regex '{regex}' successfully converted to NFA")
                
                with col2:
                    st.markdown("### 🧪 **Test Result**")
                    if result:
                        st.balloons()
                        st.success(f"🎉 **ACCEPTED!** String '{test_string}' matches the regex")
                    else:
                        st.error(f"❌ **REJECTED!** String '{test_string}' does not match the regex")
                
                # Visualize the NFA
                st.markdown("---")
                st.markdown("### 🔍 **NFA Structure Visualization**")
                
                # Get NFA visual representation
                nfa_visual = nfa.get_visual_representation()
                
                # Display NFA statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total States", nfa_visual["num_states"])
                with col2:
                    st.metric("Alphabet Size", len(nfa_visual["alphabet"]))
                with col3:
                    st.metric("Has ε-transitions", "Yes" if nfa_visual["has_epsilon"] else "No")
                
                # Display NFA details
                with st.expander("🔄 **NFA State Diagram**", expanded=True):
                    # Visual graph representation
                    st.markdown("#### State Diagram (Graph)")
                    graph = render_nfa(nfa_visual)
                    if graph:
                        st.graphviz_chart(graph)
                    else:
                        st.info("🖼️ Graph visualization requires Graphviz package. Please install with `pip install graphviz` and ensure Graphviz software is installed.")
                    
                    # Display transition table
                    st.markdown("#### Transition Table")
                    
                    # Create a table of transitions
                    alphabet_with_epsilon = list(nfa_visual["alphabet"]) + ["ε (epsilon)"]
                    
                    # Create header row
                    table_header = ["State"] + alphabet_with_epsilon + ["Accept State?"]
                    table_rows = []
                    
                    # Create rows for each state
                    for state in sorted(nfa_visual["states"]):
                        row = [f"**{state}**" + (" (start)" if state == nfa_visual["start_state"] else "")]
                        
                        # Add columns for each alphabet symbol
                        for symbol in nfa_visual["alphabet"]:
                            destinations = nfa_visual["transitions"].get(state, {}).get(symbol, [])
                            row.append(", ".join(sorted(destinations)) if destinations else "∅")
                        
                        # Add epsilon transitions
                        epsilon_destinations = nfa_visual["transitions"].get(state, {}).get("", [])
                        row.append(", ".join(sorted(epsilon_destinations)) if epsilon_destinations else "∅")
                        
                        # Is it an accept state?
                        row.append("✓" if state in nfa_visual["accept_states"] else "✗")
                        
                        table_rows.append(row)
                    
                    # Convert to markdown table
                    table_md = "| " + " | ".join(table_header) + " |\n"
                    table_md += "| " + " | ".join(["---"] * len(table_header)) + " |\n"
                    
                    for row in table_rows:
                        table_md += "| " + " | ".join(map(str, row)) + " |\n"
                    
                    st.markdown(table_md)
                    
                    # Visualize state transitions in text format
                    st.markdown("#### Transition Details")
                    
                    transition_details = []
                    for src in sorted(nfa_visual["transitions"].keys()):
                        for symbol, destinations in nfa_visual["transitions"][src].items():
                            symbol_display = "ε" if symbol == "" else symbol
                            for dest in sorted(destinations):
                                transition_details.append(f"{src} --({symbol_display})--> {dest}")
                    
                    # Display in columns for better readability
                    cols = st.columns(2)
                    half = len(transition_details) // 2 + len(transition_details) % 2
                    cols[0].markdown("  \n".join(transition_details[:half]))
                    cols[1].markdown("  \n".join(transition_details[half:]))
                
                # Display NFA as JSON
                with st.expander("🔧 **NFA Raw Data**"):
                    st.json(nfa_visual)
                        
        except Exception as e:
            st.error(f"❌ **Regex parsing failed:** {e}")
            st.exception(e)