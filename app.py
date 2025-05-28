import streamlit as st
import json
from main import DFA, regex_to_nfa

# Try to import graphviz, but gracefully handle if not installed
try:
    import graphviz
    HAS_GRAPHVIZ = True
except ImportError:
    HAS_GRAPHVIZ = False
    st.warning("📋 Graphviz package is not installed. Graph visualization will not be available. Install with: `pip install graphviz`")

# ===================== PAGE CONFIG & STYLING =====================
st.set_page_config(
    page_title="🤖 Automata Theory Toolkit", 
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #45B7D1, #96CEB4);
        background-size: 300% 300%;
        animation: gradient 8s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: bold;
        margin-bottom: 20px;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .subtitle {
        text-align: center;
        color: #666;
        font-style: italic;
        margin-bottom: 30px;
    }
    
    .logo-container {
        text-align: center;
        font-size: 6rem;
        margin: 20px 0;
    }
    
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin: 10px 0;
    }
    
    .author-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ===================== HELPER FUNCTIONS =====================
def visualize_nfa(nfa_visual):
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

def visualize_dfa(dfa_visual):
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

def render_dfa_transition_table(dfa_visual):
    table_header = ["State"] + sorted(dfa_visual["alphabet"]) + ["Accept State?"]
    table_rows = []

    for state in sorted(dfa_visual["states"]):
        row = [f"**{state}**" + (" (start)" if state == dfa_visual["start_state"] else "")]
        for symbol in sorted(dfa_visual["alphabet"]):
            dest = dfa_visual["transitions"].get(state, {}).get(symbol, "∅")
            row.append(dest)
        row.append("✓" if state in dfa_visual["accept_states"] else "✗")
        table_rows.append(row)

    # Convert to markdown table
    table_md = "| " + " | ".join(table_header) + " |\n"
    table_md += "| " + " | ".join(["---"] * len(table_header)) + " |\n"
    for row in table_rows:
        table_md += "| " + " | ".join(map(str, row)) + " |\n"

    st.markdown(table_md)

# ===================== HEADER & LOGO =====================
def show_header():
    st.markdown('<div class="logo-container">🤖⚡🔬</div>', unsafe_allow_html=True)
    st.markdown('<h1 class="main-header">AUTOMATA THEORY TOOLKIT</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">✨ Interactive Web Application for Theory of Languages and Automata ✨</p>', unsafe_allow_html=True)
    
    # Badges
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div align="center">
            <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python">
            <img src="https://img.shields.io/badge/Streamlit-%23FE4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
            <img src="https://img.shields.io/badge/Made%20with-❤️-red?style=flat-square" alt="Made with Love">
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")

# ===================== AUTHORS PAGE =====================
def authors_page():
    st.markdown('<div class="logo-container">👥💫</div>', unsafe_allow_html=True)
    st.markdown('<h1 class="main-header">MEET THE TEAM</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">🌟 The Amazing Developers Behind This Project 🌟</p>', unsafe_allow_html=True)
    
    # Team statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("👨‍💻 Team Members", "5", "")
    with col2:
        st.metric("🎓 Semester", "4", "")
    with col3:
        st.metric("📚 Course", "TBA", "")
    with col4:
        st.metric("⭐ Lines of Code", "500+", "")
    
    st.markdown("---")
    
    # Authors data
    authors = [
        {
            "name": "Nama Author 1",
            "nim": "123456789",
            "role": "🚀 Project Lead & Backend Dev",
            "github": "author1",
            "email": "author1@email.com",
            "avatar": "🧑‍💻",
        },
        {
            "name": "Nama Author 2", 
            "nim": "123456790",
            "role": "🎨 Frontend Dev & UI/UX",
            "github": "author2",
            "email": "author2@email.com", 
            "avatar": "👩‍🎨",
        },
        {
            "name": "Dunhill William Putra",
            "nim": "L0123045", 
            "role": "🧮 Algorithm Specialist",
            "github": "williamu04",
            "email": "author3@email.com",
            "avatar": "🧑‍🔬",
        },
        {
            "name": "Havizhan Rhaiya Ardhana",
            "nim": "L0123063",
            "role": "🧪 Testing & Documentation", 
            "github": "Havizhan",
            "email": "havizhanrhaiya@student.uns.ac.id",
            "avatar": "👨‍🔧",
        },
        {
            "name": "Ivan Wahyu Nugroho",
            "nim": "L0123068",
            "role": "Front End Development",
            "github": "ifwhy", 
            "email": "ifanugrh02@student.uns.ac.id",
            "avatar": "👩‍🔬",
        }
    ]
    
    # Display authors in grid
    for i in range(0, len(authors), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j < len(authors):
                author = authors[i + j]
                with col:
                    st.markdown(f"""
                    <div class="author-card">
                        <div style="font-size: 3rem; margin-bottom: 10px;">{author['avatar']}</div>
                        <h3>{author['name']}</h3>
                        <p><strong>NIM:</strong> {author['nim']}</p>
                        <p><strong>Role:</strong> {author['role']}</p>
                        <p>
                            <a href="https://github.com/{author['github']}" target="_blank" style="color: white; text-decoration: none;">
                                🔗 GitHub Profile
                            </a>
                        </p>
                        <p>📧 {author['email']}</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Team message
    st.markdown("""
    <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white; margin: 20px 0;">
        <h3>🎉 Thank You for Using Our Application! 🎉</h3>
        <p>This project was built with passion and dedication for the Theory of Languages and Automata course.</p>
        <p><strong>✨ "Learning automata theory has never been this interactive!" ✨</strong></p>
        <p>🚀 Keep coding, keep learning! 🚀</p>
    </div>
    """, unsafe_allow_html=True)

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

# ===================== TAB FUNCTIONS =====================
def dfa_simulator_tab():
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
            graph = visualize_dfa(dfa_visual)
            if graph:
                st.graphviz_chart(graph)
            else:
                st.info("🖼️ Graph visualization requires Graphviz package. Please install with `pip install graphviz` and ensure Graphviz software is installed.")
            
            # Display transition table
            st.markdown("#### Transition Table")
            render_dfa_transition_table(dfa_visual)
    
    if test_button and dfa and test_string is not None:
        with st.spinner('🔄 Running DFA simulation...'):
            result = dfa.simulate(test_string)
            if result:
                st.balloons()
                st.success(f"🎉 **ACCEPTED!** String '{test_string}' is accepted by the DFA")
            else:
                st.error(f"❌ **REJECTED!** String '{test_string}' is not accepted by the DFA")

def dfa_minimizer_tab():
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
                graph1 = visualize_dfa(vis1)
                if graph1:
                    st.graphviz_chart(graph1)
                else:
                    st.info("Graphviz not available for Original DFA.")

            with col2:
                st.markdown("### ✨ Minimized DFA")
                st.metric("States", len(minimized.states))
                st.metric("Accept States", len(minimized.accept_states))
                graph2 = visualize_dfa(vis2)
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


def regex_to_nfa_tab():
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
                    graph = visualize_nfa(nfa_visual)
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

def dfa_equivalence_tab():
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

                graph1 = visualize_dfa(vis1)
                if graph1:
                    st.graphviz_chart(graph1)
                else:
                    st.info("Graphviz not available for DFA 1.")

                st.markdown("##### 🔄 Transition Table DFA 1")
                render_dfa_transition_table(vis1)

            with col_right:
                st.markdown("#### 🅱️ DFA 2")
                st.metric("Total States", vis2["num_states"])
                st.metric("Accept States", len(vis2["accept_states"]))
                st.metric("Complete DFA", "Yes" if vis2["is_complete"] else "No")

                graph2 = visualize_dfa(vis2)
                if graph2:
                    st.graphviz_chart(graph2)
                else:
                    st.info("Graphviz not available for DFA 2.")

                st.markdown("##### 🔄 Transition Table DFA 2")
                render_dfa_transition_table(vis2)


# ===================== MAIN APPLICATION =====================
def main():
    # Show header on all pages
    show_header()
    
    # Sidebar navigation with beautiful styling
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h2 style="color: #4ECDC4;">🧭 Navigation</h2>
        <p style="color: #666;">Choose your tool below</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab = st.sidebar.radio(
        "Select Tool", 
        [
            "🏠 Home",
            "🔁 DFA String Testing", 
            "🔤 Regex to NFA", 
            "🔽 DFA Minimization",
            "⚖️ DFA Equivalence",
            "👥 Meet the Team"
        ],
        index=0
    )
    
    # Add some sidebar info
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 15px; border-radius: 10px; color: white; text-align: center;">
        <h4>📚 Quick Help</h4>
        <p><small>Select a tool from above to start working with automata!</small></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Route to different pages
    if tab == "🏠 Home":
        home_page()
    elif tab == "🔁 DFA String Testing":
        dfa_simulator_tab()
    elif tab == "🔤 Regex to NFA":
        regex_to_nfa_tab()
    elif tab == "🔽 DFA Minimization":
        dfa_minimizer_tab()
    elif tab == "⚖️ DFA Equivalence":
        dfa_equivalence_tab()
    elif tab == "👥 Meet the Team":
        authors_page()

def home_page():
    st.markdown('<div class="logo-container">🏠</div>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; color: #4ECDC4;">Welcome to Automata Theory Toolkit</h2>', unsafe_allow_html=True)
    
    # Feature overview
    st.markdown("## 🎯 What Can You Do Here?")
    
    features = [
        ("🔁", "DFA String Testing", "Test if a string is accepted by your Deterministic Finite Automaton"),
        ("🔤", "Regex to NFA", "Convert Regular Expressions to Non-deterministic Finite Automata and test strings"),
        ("🔽", "DFA Minimization", "Optimize your DFA by reducing the number of states using Hopcroft's algorithm"),
        ("⚖️", "DFA Equivalence", "Check if two DFAs are equivalent and accept the same language"),
        ("👥", "Meet the Team", "Learn about the developers who created this amazing tool")
    ]
    
    for i, (icon, title, desc) in enumerate(features):
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown(f'<div style="font-size: 3rem; text-align: center;">{icon}</div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f"### {title}")
            st.markdown(desc)
        
        if i < len(features) - 1:
            st.markdown("---")
    
    # Getting started section
    st.markdown("---")
    st.markdown("## 🚀 Getting Started")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>1️⃣ Choose a Tool</h4>
            <p>Select from the sidebar which automata operation you want to perform</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>2️⃣ Configure</h4>
            <p>Input your DFA parameters or regex according to the selected tool</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h4>3️⃣ Execute</h4>
            <p>Run the simulation and see the results instantly with visual feedback</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
