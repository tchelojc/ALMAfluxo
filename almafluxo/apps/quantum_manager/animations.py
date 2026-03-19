# Crie um arquivo chamado animations.py na mesma pasta do seu projeto com este conteúdo:

import streamlit as st
import time
import random
from math import sin, cos, pi

def render_quantum_animation():
    """Animação quântica personalizada com partículas"""
    particle_html = """
    <style>
        .quantum-particle {
            position: fixed;
            width: 2px;
            height: 2px;
            background: #00FF88;
            border-radius: 50%;
            pointer-events: none;
            animation: quantum-move 2s infinite;
        }

        @keyframes quantum-move {
            0% { transform: translate(0, 0); opacity: 1; }
            100% { transform: translate(%spx, %spx); opacity: 0; }
        }
    </style>
    """ % (random.randint(-300, 300), random.randint(-300, 300))
    
    st.markdown(particle_html, unsafe_allow_html=True)
    st.components.v1.html("""
    <script>
        function createParticle() {
            const particle = document.createElement('div');
            particle.className = 'quantum-particle';
            document.body.appendChild(particle);
            
            setTimeout(() => {
                particle.remove();
            }, 2000);
        }
        
        setInterval(createParticle, 50);
    </script>
    """)