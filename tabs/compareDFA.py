import streamlit as st
from helper.inputDFA import input_dfa
from helper.visualizeTable import render_table
from helper.visualizeGraph import render_dfa

def compare_dfa():
    st.markdown('<div class="logo-container">⚖️</div>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; color: #764ba2;">DFA Equivalence Checker</h2>', unsafe_allow_html=True)

    st.markdown("### 🤖 Configure First DFA")
    dfa1 = input_dfa(index=1)

    st.markdown("---")
    st.markdown("### 🤖 Configure Second DFA") 
    dfa2 = input_dfa(index=2)

    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        compare_button = st.button("⚖️ Compare DFAs", type="primary", use_container_width=True)

    if compare_button and dfa1 and dfa2:
        with st.spinner('🔄 Comparing DFAs for equivalence...'):
            equivalent = dfa1.is_equivalent(dfa2)

            if equivalent:
                st.balloons()
                st.success("🎉 **EQUIVALENT!** Both DFAs accept the same language")
                st.markdown("""
                <div style="background: linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%); padding: 20px; border-radius: 15px; color: white; text-align: center; margin: 20px 0;">
                    <h3>✅ DFAs are Equivalent!</h3>
                    <p>The two DFAs recognize exactly the same set of strings.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("❌ **NOT EQUIVALENT!** The DFAs accept different languages")
                st.markdown("""
                <div style="background: linear-gradient(135deg, #FF6B6B 0%, #EE5A6F 100%); padding: 20px; border-radius: 15px; color: white; text-align: center; margin: 20px 0;">
                    <h3>❌ DFAs are Not Equivalent!</h3>
                    <p>The two DFAs recognize different sets of strings.</p>
                </div>
                """, unsafe_allow_html=True)

            # --- Visualisasi kedua DFA ---
            st.markdown("### 🧭 Visual Comparison of Both DFAs")

            vis1 = dfa1.get_visual_representation()
            vis2 = dfa2.get_visual_representation()

            col_left, col_right = st.columns(2)

            with col_left:
                st.markdown("#### 🅰️ DFA 1")
                st.metric("Total States", vis1["num_states"])
                st.metric("Accept States", len(vis1["accept_states"]))
                st.metric("Complete DFA", "Yes" if vis1["is_complete"] else "No")

                render_dfa(vis1)

                st.markdown("##### 🔄 Transition Table DFA 1")
                render_table(vis1)

            with col_right:
                st.markdown("#### 🅱️ DFA 2")
                st.metric("Total States", vis2["num_states"])
                st.metric("Accept States", len(vis2["accept_states"]))
                st.metric("Complete DFA", "Yes" if vis2["is_complete"] else "No")

                render_dfa(vis2)

                st.markdown("##### 🔄 Transition Table DFA 2")
                render_table(vis2)
