"""
📄 Page Components for Automata Theory Toolkit
===============================================
Modular page components with Tailwind styling
"""

import streamlit as st
import json
from main import DFA, regex_to_nfa
from components.ui_components import TailwindComponents

class Pages:
    """Collection of page components"""
    
    @staticmethod
    def home_page():
        """🏠 Home page content"""
        TailwindComponents.page_header(
            "Welcome to Automata Theory Toolkit", 
            "🏠",
            "Choose a tool from the sidebar to get started!"
        )
        
        # Feature overview section
        st.markdown("## 🎯 What Can You Do Here?")
        
        # Features grid
        col1, col2 = st.columns(2)
        
        with col1:
            TailwindComponents.feature_card(
                "🔁", 
                "DFA String Testing",
                "Test if a string is accepted by your Deterministic Finite Automaton",
                "blue"
            )
            
        with col2:
            TailwindComponents.feature_card(
                "🔤", 
                "Regex to NFA",
                "Convert Regular Expressions to Non-deterministic Finite Automata",
                "green"
            )
        
        col3, col4 = st.columns(2)
        
        with col3:
            TailwindComponents.feature_card(
                "🔽", 
                "DFA Minimization",
                "Optimize your DFA by reducing the number of states",
                "red"
            )
            
        with col4:
            TailwindComponents.feature_card(
                "⚖️", 
                "DFA Equivalence",
                "Check if two DFAs are equivalent and accept the same language",
                "purple"
            )
        
        # Getting started section
        st.markdown("---")
        st.markdown("## 🚀 Getting Started")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            TailwindComponents.feature_card(
                "1️⃣", 
                "Choose a Tool",
                "Select from the sidebar which automata operation you want to perform",
                "blue"
            )
        
        with col2:
            TailwindComponents.feature_card(
                "2️⃣", 
                "Configure",
                "Input your DFA parameters or regex according to the selected tool",
                "green"
            )
        
        with col3:
            TailwindComponents.feature_card(
                "3️⃣", 
                "Execute",
                "Run the simulation and see the results instantly with visual feedback",
                "purple"
            )
    
    @staticmethod
    def authors_page():
        """👥 Team page content"""
        TailwindComponents.page_header(
            "Meet the Team", 
            "👥💫",
            "The Amazing Developers Behind This Project"
        )
        
        # Team statistics
        st.markdown("### 📊 Team Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            TailwindComponents.metric_card("👨‍💻", "Team Members", "5", "blue")
        with col2:
            TailwindComponents.metric_card("🎓", "Semester", "4", "green")
        with col3:
            TailwindComponents.metric_card("📚", "Course", "TBA", "purple")
        with col4:
            TailwindComponents.metric_card("⭐", "Lines of Code", "500+", "red")
        
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
                "name": "Nama Author 4",
                "nim": "123456792",
                "role": "🧪 Testing & Documentation", 
                "github": "author4",
                "email": "author4@email.com",
                "avatar": "👨‍🔧",
            },
            {
                "name": "Ivan Wahyu Nugroho",
                "nim": "L0123068",
                "role": "🎨 Front End Development",
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
                        TailwindComponents.author_card(
                            author['name'],
                            author['nim'],
                            author['role'],
                            author['github'],
                            author['email'],
                            author['avatar']
                        )
        
        # Team message
        st.markdown("---")
        from streamlit_tailwind import st_tailwind
        st_tailwind(
            """
            <div class="bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl p-8 text-white text-center shadow-xl">
                <h3 class="text-2xl font-bold mb-4">🎉 Thank You for Using Our Application! 🎉</h3>
                <p class="mb-4">This project was built with passion and dedication for the Theory of Languages and Automata course.</p>
                <p class="text-lg font-semibold mb-4">✨ "Learning automata theory has never been this interactive!" ✨</p>
                <p class="text-xl">🚀 Keep coding, keep learning! 🚀</p>
            </div>
            """
        )
