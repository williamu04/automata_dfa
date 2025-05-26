"""
🎨 UI Components with Tailwind CSS for Automata Theory Toolkit
=============================================================
Modern, responsive components using Tailwind CSS classes
"""

import streamlit as st
from streamlit_tailwind import st_tailwind

class TailwindComponents:
    """Collection of reusable Tailwind CSS components"""
    
    @staticmethod
    def header():
        """🚀 Main header component with animated gradient text"""
        st_tailwind(
            """
            <div class="text-center py-8">
                <!-- Animated Robot Icons -->
                <div class="text-8xl mb-6 animate-bounce">
                    🤖⚡🔬
                </div>
                
                <!-- Main Title with Gradient Animation -->
                <h1 class="text-6xl font-black mb-4 bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 bg-clip-text text-transparent animate-pulse">
                    AUTOMATA THEORY TOOLKIT
                </h1>
                
                <!-- Subtitle -->
                <p class="text-xl text-gray-600 italic mb-8">
                    ✨ Interactive Web Application for Theory of Languages and Automata ✨
                </p>
                
                <!-- Tech Badges -->
                <div class="flex justify-center gap-4 mb-8">
                    <span class="bg-blue-500 text-white px-4 py-2 rounded-full font-semibold shadow-lg hover:shadow-xl transition-shadow">
                        🐍 Python
                    </span>
                    <span class="bg-red-500 text-white px-4 py-2 rounded-full font-semibold shadow-lg hover:shadow-xl transition-shadow">
                        🎨 Streamlit
                    </span>
                    <span class="bg-pink-500 text-white px-4 py-2 rounded-full font-semibold shadow-lg hover:shadow-xl transition-shadow">
                        ❤️ Made with Love
                    </span>
                </div>
                
                <!-- Separator -->
                <hr class="border-2 border-gradient-to-r from-purple-400 to-pink-400 rounded">
            </div>
            """
        )
    
    @staticmethod
    def feature_card(icon, title, description, color="blue"):
        """🎯 Feature card component"""
        color_classes = {
            "blue": "from-blue-500 to-purple-600",
            "green": "from-green-500 to-teal-600", 
            "red": "from-red-500 to-pink-600",
            "yellow": "from-yellow-500 to-orange-600",
            "purple": "from-purple-500 to-indigo-600"
        }
        
        gradient = color_classes.get(color, color_classes["blue"])
        
        st_tailwind(
            f"""
            <div class="bg-gradient-to-br {gradient} rounded-xl p-6 text-white shadow-xl hover:shadow-2xl transform hover:-translate-y-2 transition-all duration-300 cursor-pointer">
                <div class="text-4xl mb-4 text-center">{icon}</div>
                <h3 class="text-2xl font-bold mb-3 text-center">{title}</h3>
                <p class="text-white/90 text-center leading-relaxed">{description}</p>
            </div>
            """
        )
    
    @staticmethod
    def input_card(title, icon):
        """📝 Input configuration card"""
        st_tailwind(
            f"""
            <div class="bg-white rounded-xl shadow-lg border border-gray-200 p-6 mb-6">
                <div class="flex items-center mb-4">
                    <span class="text-3xl mr-3">{icon}</span>
                    <h3 class="text-2xl font-bold text-gray-800">{title}</h3>
                </div>
                <div class="text-gray-600">Configure your automaton parameters below</div>
            </div>
            """
        )
    
    @staticmethod
    def success_alert(message):
        """✅ Success alert component"""
        st_tailwind(
            f"""
            <div class="bg-gradient-to-r from-green-400 to-green-600 text-white p-4 rounded-lg shadow-lg mb-4 animate-pulse">
                <div class="flex items-center">
                    <span class="text-2xl mr-3">🎉</span>
                    <div>
                        <p class="font-bold">SUCCESS!</p>
                        <p>{message}</p>
                    </div>
                </div>
            </div>
            """
        )
    
    @staticmethod
    def error_alert(message):
        """❌ Error alert component"""
        st_tailwind(
            f"""
            <div class="bg-gradient-to-r from-red-400 to-red-600 text-white p-4 rounded-lg shadow-lg mb-4">
                <div class="flex items-center">
                    <span class="text-2xl mr-3">❌</span>
                    <div>
                        <p class="font-bold">ERROR!</p>
                        <p>{message}</p>
                    </div>
                </div>
            </div>
            """
        )
    
    @staticmethod
    def info_alert(message):
        """ℹ️ Info alert component"""
        st_tailwind(
            f"""
            <div class="bg-gradient-to-r from-blue-400 to-blue-600 text-white p-4 rounded-lg shadow-lg mb-4">
                <div class="flex items-center">
                    <span class="text-2xl mr-3">ℹ️</span>
                    <div>
                        <p class="font-bold">INFO</p>
                        <p>{message}</p>
                    </div>
                </div>
            </div>
            """
        )
    
    @staticmethod
    def metric_card(icon, label, value, color="blue"):
        """📊 Metric display card"""
        color_classes = {
            "blue": "from-blue-500 to-blue-600",
            "green": "from-green-500 to-green-600",
            "red": "from-red-500 to-red-600",
            "purple": "from-purple-500 to-purple-600"
        }
        
        gradient = color_classes.get(color, color_classes["blue"])
        
        st_tailwind(
            f"""
            <div class="bg-gradient-to-br {gradient} rounded-xl p-6 text-white shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300">
                <div class="text-center">
                    <div class="text-4xl mb-2">{icon}</div>
                    <div class="text-3xl font-bold mb-1">{value}</div>
                    <div class="text-white/80 text-sm">{label}</div>
                </div>
            </div>
            """
        )
    
    @staticmethod
    def button(text, onclick=None, variant="primary", icon=""):
        """🔘 Custom button component"""
        variants = {
            "primary": "bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600",
            "secondary": "bg-gradient-to-r from-gray-500 to-gray-600 hover:from-gray-600 hover:to-gray-700",
            "success": "bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700",
            "danger": "bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700"
        }
        
        style = variants.get(variant, variants["primary"])
        
        st_tailwind(
            f"""
            <button class="{style} text-white font-bold py-3 px-6 rounded-lg shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-300 w-full">
                {icon} {text}
            </button>
            """
        )
    
    @staticmethod
    def author_card(name, nim, role, github, email, avatar):
        """👤 Author profile card"""
        st_tailwind(
            f"""
            <div class="bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 rounded-xl p-6 text-white shadow-xl hover:shadow-2xl transform hover:-translate-y-2 hover:rotate-1 transition-all duration-300 cursor-pointer">
                <div class="text-center">
                    <div class="text-6xl mb-4">{avatar}</div>
                    <h3 class="text-xl font-bold mb-2">{name}</h3>
                    <p class="text-white/90 mb-1"><strong>NIM:</strong> {nim}</p>
                    <p class="text-white/90 mb-3">{role}</p>
                    <div class="space-y-2">
                        <a href="https://github.com/{github}" target="_blank" 
                           class="block bg-white/20 hover:bg-white/30 rounded-lg py-2 px-4 transition-colors">
                            🔗 GitHub Profile
                        </a>
                        <p class="text-sm text-white/80">📧 {email}</p>
                    </div>
                </div>
            </div>
            """
        )
    
    @staticmethod
    def page_header(title, icon, subtitle=""):
        """📄 Page header component"""
        st_tailwind(
            f"""
            <div class="text-center mb-8">
                <div class="text-7xl mb-4 animate-bounce">{icon}</div>
                <h2 class="text-4xl font-bold text-gray-800 mb-2">{title}</h2>
                {f'<p class="text-lg text-gray-600">{subtitle}</p>' if subtitle else ''}
            </div>
            """
        )
    
    @staticmethod
    def sidebar_nav():
        """🧭 Sidebar navigation styling"""
        st_tailwind(
            """
            <style>
                .css-1d391kg {
                    background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
                    border-radius: 0 25px 25px 0;
                }
                
                .css-1d391kg .stRadio > div {
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 15px;
                    margin: 10px 0;
                    padding: 10px;
                }
                
                .css-1d391kg .stRadio label {
                    color: white !important;
                    font-weight: 600;
                }
            </style>
            """
        )
    
    @staticmethod
    def loading_spinner(text="Loading..."):
        """⏳ Loading spinner component"""
        st_tailwind(
            f"""
            <div class="flex items-center justify-center p-8">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-500 mr-4"></div>
                <span class="text-lg text-gray-600">{text}</span>
            </div>
            """
        )
