import streamlit as st
import json
from main import DFA, regex_to_nfa

st.set_page_config(page_title="Teori Bahasa Automata", layout="wide")

st.title("🧠 Automata Simulator")

def input_dfa(index=1):
    st.subheader(f"DFA #{index}")
    states = st.text_input(f"[DFA {index}] States (comma-separated)", "q0,q1")
    alphabet = st.text_input(f"[DFA {index}] Alphabet (comma-separated)", "a,b")
    start_state = st.text_input(f"[DFA {index}] Start State", "q0")
    accept_states = st.text_input(f"[DFA {index}] Accept States (comma-separated)", "q1")
    transitions_json = st.text_area(f"[DFA {index}] Transitions (JSON format)", 
        '{\n  "q0": {"a": "q1", "b": "q0"},\n  "q1": {"a": "q1", "b": "q0"}\n}')
    
    try:
        transitions = json.loads(transitions_json)
        dfa = DFA(
            states=states.split(","),
            alphabet=alphabet.split(","),
            start_state=start_state,
            accept_states=accept_states.split(","),
            transitions=transitions
        )
        return dfa
    except Exception as e:
        st.error(f"Error parsing DFA {index}: {e}")
        return None

def dfa_simulator_tab():
    st.header("🔁 Input DFA dan uji string")
    dfa = input_dfa(index=1)
    test_string = st.text_input("String uji", "")

    if st.button("Simulasikan DFA"):
        if dfa:
            result = dfa.simulate(test_string)
            st.success("✅ Diterima!" if result else "❌ Ditolak.")

def dfa_minimizer_tab():
    st.header("🔽 Minimisasi DFA")
    dfa = input_dfa(index=1)

    if st.button("Minimize DFA"):
        if dfa:
            minimized = dfa.minimize()
            st.subheader("📉 DFA yang diminimisasi")
            st.json({
                "states": list(minimized.states),
                "start_state": minimized.start_state,
                "accept_states": list(minimized.accept_states),
                "transitions": minimized.transitions
            })

def regex_to_nfa_tab():
    st.header("🔤 Input Regex → Bangun NFA → Uji string")
    regex = st.text_input("Masukkan Regular Expression (a, b, |, *, ())", "a(b|a)*")
    test_string = st.text_input("String uji", "")

    if st.button("Convert and Test NFA"):
        try:
            nfa = regex_to_nfa(regex)
            result = nfa.simulate(test_string)
            st.success("✅ Diterima!" if result else "❌ Ditolak.")
        except Exception as e:
            st.error(f"Regex parsing failed: {e}")

def dfa_equivalence_tab():
    st.header("⚖️ Cek Ekuivalensi Dua DFA")

    dfa1 = input_dfa(index=1)
    st.divider()
    dfa2 = input_dfa(index=2)

    if st.button("Compare DFA 1 and DFA 2"):
        if dfa1 and dfa2:
            equivalent = dfa1.is_equivalent(dfa2)
            st.success("✅ Kedua DFA Ekuivalen.") if equivalent else st.error("❌ Kedua DFA Tidak Ekuivalen.")

def main():
    tab = st.sidebar.radio("Select Tool", [
        "Input DFA dan uji string", 
        "Input Regex → Bangun NFA → Uji string", 
        "Minimisasi DFA",
        "Cek Ekuivalensi Dua DFA"
    ])

    if tab == "Input DFA dan uji string":
        dfa_simulator_tab()
    elif tab == "Input Regex → Bangun NFA → Uji string":
        regex_to_nfa_tab()
    elif tab == "Minimisasi DFA":
        dfa_minimizer_tab()
    elif tab == "Cek Ekuivalensi Dua DFA":
        dfa_equivalence_tab()

if __name__ == "__main__":
    main()
