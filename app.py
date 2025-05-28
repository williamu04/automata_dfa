import streamlit as st
from tabs.simulateDFA import simulate_dfa
from tabs.simulateNFA import simulate_nfa
from tabs.minimizeDFA import minimize_dfa
from tabs.compareDFA import compare_dfa


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
        simulate_dfa()
    elif tab == "🔤 Regex to NFA":
        simulate_nfa()
    elif tab == "🔽 DFA Minimization":
        minimize_dfa()
    elif tab == "⚖️ DFA Equivalence":
        compare_dfa()
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
