"""
🔧 DFA Component - Modular DFA operations with Tailwind styling
===============================================================
"""

import streamlit as st
import json
from engines.REGEX import DFA
from components.ui_components import TailwindComponents

class DFAComponent:
    """DFA operations component"""
    
    @staticmethod
    def input_dfa(index=1):
        """📝 DFA input form component"""
        TailwindComponents.input_card(f"DFA Configuration #{index}", "⚙️")
        
        col1, col2 = st.columns(2)
        
        with col1:
            states = st.text_input(
                "🔘 States (comma-separated)", 
                "q0,q1", 
                key=f"states_{index}",
                help="Enter state names separated by commas"
            )
            alphabet = st.text_input(
                "🔤 Alphabet (comma-separated)", 
                "a,b", 
                key=f"alphabet_{index}",
                help="Enter alphabet symbols separated by commas"
            )
        
        with col2:
            start_state = st.text_input(
                "▶️ Start State", 
                "q0", 
                key=f"start_{index}",
                help="Enter the initial state"
            )
            accept_states = st.text_input(
                "✅ Accept States (comma-separated)", 
                "q1", 
                key=f"accept_{index}",
                help="Enter accepting states separated by commas"
            )
        
        st.markdown("**🔄 Transition Function (JSON format):**")
        transitions_json = st.text_area(
            f"Define transitions for DFA {index}", 
            '{\n  "q0": {"a": "q1", "b": "q0"},\n  "q1": {"a": "q1", "b": "q0"}\n}',
            height=150,
            key=f"transitions_{index}",
            help="Define state transitions in JSON format"
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
            TailwindComponents.success_alert(f"DFA {index} configured successfully!")
            return dfa
        except Exception as e:
            TailwindComponents.error_alert(f"Error parsing DFA {index}: {e}")
            return None
    
    @staticmethod
    def simulator_page():
        """🔁 DFA String Testing page"""
        TailwindComponents.page_header(
            "DFA String Testing", 
            "🔁",
            "Test if strings are accepted by your Deterministic Finite Automaton"
        )
        
        dfa = DFAComponent.input_dfa(index=1)
        
        st.markdown("---")
        st.markdown("### 🧪 Test Your String")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            test_string = st.text_input(
                "🔤 Enter string to test", 
                "", 
                placeholder="Enter your test string here...",
                help="Input the string you want to test against the DFA"
            )
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            test_button = st.button(
                "🚀 Run Simulation", 
                type="primary", 
                use_container_width=True
            )
        
        if test_button and dfa and test_string is not None:
            with st.spinner('🔄 Running DFA simulation...'):
                result = dfa.simulate(test_string)
                if result:
                    st.balloons()
                    TailwindComponents.success_alert(
                        f"String '{test_string}' is ACCEPTED by the DFA"
                    )
                else:
                    TailwindComponents.error_alert(
                        f"String '{test_string}' is REJECTED by the DFA"
                    )
    
    @staticmethod
    def minimizer_page():
        """🔽 DFA Minimization page"""
        TailwindComponents.page_header(
            "DFA Minimization", 
            "🔽",
            "Optimize your DFA by reducing the number of states"
        )
        
        dfa = DFAComponent.input_dfa(index=1)

        st.markdown("---")
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 📊 Original DFA")
            if dfa:
                TailwindComponents.info_alert(f"States: {len(dfa.states)}")
        
        with col2:
            st.markdown("### ⚡ Actions")
            minimize_button = st.button(
                "🔧 Minimize DFA", 
                type="primary", 
                use_container_width=True
            )

        if minimize_button and dfa:
            with st.spinner('🔄 Minimizing DFA...'):
                minimized = dfa.minimize()
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("### 📉 **Minimized DFA Result**")
                    st.json({
                        "states": list(minimized.states),
                        "start_state": minimized.start_state,
                        "accept_states": list(minimized.accept_states),
                        "transitions": minimized.transitions
                    })
                
                with col2:
                    st.markdown("### 📈 **Optimization Stats**")
                    original_states = len(dfa.states)
                    minimized_states = len(minimized.states)
                    reduction = ((original_states - minimized_states) / original_states * 100) if original_states > 0 else 0
                    
                    TailwindComponents.metric_card("📊", "Original States", str(original_states), "blue")
                    st.markdown("<br>", unsafe_allow_html=True)
                    TailwindComponents.metric_card("⚡", "Minimized States", str(minimized_states), "green")
                    st.markdown("<br>", unsafe_allow_html=True)
                    TailwindComponents.metric_card("📉", "Reduction", f"{reduction:.1f}%", "purple")
    
    @staticmethod
    def equivalence_page():
        """⚖️ DFA Equivalence page"""
        TailwindComponents.page_header(
            "DFA Equivalence Checker", 
            "⚖️",
            "Check if two DFAs are equivalent and accept the same language"
        )

        st.markdown("### 🤖 Configure First DFA")
        dfa1 = DFAComponent.input_dfa(index=1)
        
        st.markdown("---")
        st.markdown("### 🤖 Configure Second DFA") 
        dfa2 = DFAComponent.input_dfa(index=2)
        
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            compare_button = st.button(
                "⚖️ Compare DFAs", 
                type="primary", 
                use_container_width=True
            )

        if compare_button and dfa1 and dfa2:
            with st.spinner('🔄 Comparing DFAs for equivalence...'):
                equivalent = dfa1.is_equivalent(dfa2)
                
                if equivalent:
                    st.balloons()
                    TailwindComponents.success_alert(
                        "EQUIVALENT! Both DFAs accept the same language"
                    )
                    from streamlit_tailwind import st_tailwind
                    st_tailwind(
                        """
                        <div class="bg-gradient-to-r from-green-400 to-green-600 rounded-xl p-8 text-white text-center shadow-xl">
                            <h3 class="text-2xl font-bold mb-4">✅ DFAs are Equivalent!</h3>
                            <p class="text-lg">The two DFAs recognize exactly the same set of strings.</p>
                        </div>
                        """
                    )
                else:
                    TailwindComponents.error_alert(
                        "NOT EQUIVALENT! The DFAs accept different languages"
                    )
                    from streamlit_tailwind import st_tailwind
                    st_tailwind(
                        """
                        <div class="bg-gradient-to-r from-red-400 to-red-600 rounded-xl p-8 text-white text-center shadow-xl">
                            <h3 class="text-2xl font-bold mb-4">❌ DFAs are Not Equivalent!</h3>
                            <p class="text-lg">The two DFAs recognize different sets of strings.</p>
                        </div>
                        """
                    )
