import streamlit as st
import os
import time
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from tempfile import NamedTemporaryFile
import numpy as np

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="🧠 NeoSearch AI", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")

# ---------------- ULTIMATE CYBERPUNK CSS ----------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;700;900&display=swap');
    
    /* ROOT ANIMATIONS */
    @keyframes neonGlow {
        0%, 100% { text-shadow: 0 0 5px #00f2fe, 0 0 10px #00f2fe, 0 0 15px #00f2fe; }
        50% { text-shadow: 0 0 20px #00f2fe, 0 0 30px #00f2fe, 0 0 40px #00f2fe; }
    }
    
    @keyframes cyberPulse {
        0%, 100% { box-shadow: 0 0 10px #00f2fe; }
        50% { box-shadow: 0 0 30px #00f2fe, 0 0 50px #00f2fe; }
    }
    
    @keyframes matrixRain {
        0% { background-position: 0 0; }
        100% { background-position: 100% 100%; }
    }
    
    @keyframes floatUp {
        0% { opacity: 0; transform: translateY(50px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes scanline {
        0% { transform: translateY(-100%); }
        100% { transform: translateY(100%); }
    }
    
    /* GLOBAL STYLES */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
        background-size: 400% 400%;
        animation: matrixRain 20s linear infinite;
        font-family: 'Inter', sans-serif;
        overflow-x: hidden;
    }
    
    /* NEON TEXT */
    .neon-text {
        font-family: 'Orbitron', monospace;
        font-weight: 900;
        background: linear-gradient(45deg, #00f2fe, #4facfe, #00f2fe);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: neonGlow 2s ease-in-out infinite alternate, 
                   cyberPulse 3s ease-in-out infinite;
        text-shadow: 0 0 20px rgba(0, 242, 254, 0.5);
    }
    
    /* HERO SECTION */
    .hero-section {
        background: linear-gradient(135deg, rgba(0, 242, 254, 0.1) 0%, rgba(79, 172, 254, 0.1) 100%);
        border: 2px solid transparent;
        background-clip: padding-box;
        border-radius: 30px;
        padding: 4rem;
        margin-bottom: 3rem;
        position: relative;
        overflow: hidden;
        animation: cyberPulse 4s ease-in-out infinite;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(0, 242, 254, 0.1), transparent);
        animation: scanline 3s linear infinite;
    }
    
    .hero-title {
        font-size: 4.5rem !important;
        font-weight: 900 !important;
        margin: 0;
        animation: floatUp 1s ease-out;
    }
    
    .hero-subtitle {
        font-size: 1.4rem !important;
        color: #a0a0ff !important;
        font-weight: 400;
        margin-top: 1rem;
        animation: floatUp 1s ease-out 0.3s both;
    }
    
    /* PREMIUM BUTTONS */
    .cyber-btn {
        background: linear-gradient(45deg, #00f2fe, #4facfe);
        color: #000 !important;
        border: none;
        border-radius: 15px;
        padding: 12px 30px;
        font-weight: 900;
        font-size: 1.1rem;
        font-family: 'Orbitron', monospace;
        text-transform: uppercase;
        letter-spacing: 2px;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
        box-shadow: 0 10px 30px rgba(0, 242, 254, 0.3);
    }
    
    .cyber-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 20px 40px rgba(0, 242, 254, 0.5);
        animation: cyberPulse 0.5s infinite;
    }
    
    .cyber-btn:active {
        transform: translateY(-1px);
    }
    
    /* ULTIMATE RESULT CARDS */
    .result-card {
        background: rgba(17, 17, 17, 0.9);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 242, 254, 0.3);
        border-radius: 25px;
        padding: 2rem;
        margin-bottom: 2rem;
        position: relative;
        animation: floatUp 0.8s ease-out forwards;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        overflow: hidden;
    }
    
    .result-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #00f2fe, #4facfe, #00f2fe);
        background-size: 200% 100%;
        animation: cyberPulse 2s ease-in-out infinite;
    }
    
    .result-card:hover {
        transform: translateY(-10px) scale(1.02);
        border-color: #00f2fe;
        box-shadow: 0 25px 50px rgba(0, 242, 254, 0.3);
    }
    
    .result-header {
        font-family: 'Orbitron', monospace;
        font-size: 1.2rem !important;
        font-weight: 900 !important;
        background: linear-gradient(45deg, #00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    
    .score-badge {
        background: linear-gradient(45deg, #00f2fe, #4facfe);
        color: #000 !important;
        padding: 8px 20px;
        border-radius: 50px;
        font-weight: 900;
        font-size: 0.9rem;
        font-family: 'Orbitron', monospace;
        display: inline-block;
        animation: cyberPulse 2s infinite;
    }
    
    /* STAT CARDS */
    .stat-card {
        background: rgba(17, 17, 17, 0.8);
        backdrop-filter: blur(20px);
        border: 2px solid rgba(0, 242, 254, 0.2);
        border-radius: 25px;
        padding: 2.5rem;
        text-align: center;
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stat-card:hover {
        border-color: #00f2fe;
        transform: translateY(-10px);
        box-shadow: 0 30px 60px rgba(0, 242, 254, 0.2);
    }
    
    .stat-number {
        font-family: 'Orbitron', monospace;
        font-size: 4rem !important;
        font-weight: 900 !important;
        background: linear-gradient(45deg, #00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        animation: cyberPulse 2s infinite;
    }
    
    /* INPUT FIELDS */
    .stTextInput > div > div > input {
        background: rgba(17, 17, 17, 0.9) !important;
        color: #fff !important;
        border: 2px solid rgba(0, 242, 254, 0.3) !important;
        border-radius: 15px !important;
        padding: 15px 20px !important;
        font-size: 1.1rem;
        backdrop-filter: blur(20px);
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #00f2fe !important;
        box-shadow: 0 0 30px rgba(0, 242, 254, 0.5) !important;
        transform: scale(1.02);
    }
    
    /* TABS */
    .stTabs [data-baseweb="tab"] {
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        font-size: 1.2rem;
        color: rgba(255,255,255,0.6) !important;
        padding: 15px 30px;
        border-radius: 15px;
        margin: 0 10px;
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    
    .stTabs [aria-selected="true"] {
        color: #00f2fe !important;
        background: rgba(0, 242, 254, 0.1) !important;
        border-color: #00f2fe !important;
        box-shadow: 0 0 20px rgba(0, 242, 254, 0.3);
    }
    
    /* SPINNER */
    .stSpinner {
        border-color: #00f2fe !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- PARTICLE BACKGROUND ----------------
def particle_background():
    st.markdown("""
    <div style="
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
    ">
        <canvas id="particles"></canvas>
    </div>
    <script>
        function createParticles() {
            const canvas = document.getElementById('particles');
            const ctx = canvas.getContext('2d');
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            
            const particles = [];
            for(let i = 0; i < 100; i++) {
                particles.push({
                    x: Math.random() * canvas.width,
                    y: Math.random() * canvas.height,
                    vx: (Math.random() - 0.5) * 0.5,
                    vy: (Math.random() - 0.5) * 0.5,
                    radius: Math.random() * 2 + 1
                });
            }
            
            function animate() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = 'rgba(0, 242, 254, 0.1)';
                particles.forEach(p => {
                    ctx.beginPath();
                    ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
                    ctx.fill();
                    p.x += p.vx;
                    p.y += p.vy;
                    if(p.x < 0 || p.x > canvas.width) p.vx *= -1;
                    if(p.y < 0 || p.y > canvas.height) p.vy *= -1;
                });
                requestAnimationFrame(animate);
            }
            animate();
        }
        createParticles();
    </script>
    """, unsafe_allow_html=True)

particle_background()

# ---------------- STATE MANAGEMENT ----------------
if "db" not in st.session_state:
    st.session_state.update({
        "db": None, 
        "docs": 0, 
        "chunks": 0, 
        "searches": 0, 
        "status": "🟢 READY"
    })

def process_data(files, size, overlap):
    docs = []
    for f in files:
        ext = f.name.split('.')[-1].lower()
        with NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
            tmp.write(f.read())
            path = tmp.name
        try:
            loader = PyPDFLoader(path) if ext == "pdf" else Docx2txtLoader(path) if ext == "docx" else TextLoader(path)
            docs.extend(loader.load())
        except:
            st.error(f"Failed to load {f.name}")
        finally:
            os.remove(path)
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=size, chunk_overlap=overlap)
    return splitter.split_documents(docs)

# ---------------- HERO SECTION ----------------
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title neon-text">NEOSEARCH AI</h1>
    <p class="hero-subtitle">⚡ Semantic Intelligence • Vector-Powered • Instant Discovery</p>
</div>
""", unsafe_allow_html=True)

# ---------------- PREMIUM TABS ----------------
tab1, tab2, tab3, tab4 = st.tabs(["🔍 DISCOVER", "📤 INGEST", "📊 METRICS", "⚙️ CONTROL"])

# --- TAB 1: ULTIMATE SEARCH ---
with tab1:
    col1, col2 = st.columns([5, 1])
    with col2:
        top_k = st.slider("Results", 1, 15, 5, help="Number of top matches")
    
    query = st.text_input("🔍 Enter your query", placeholder="Search across all documents...", key="search_query")
    
    if query and st.session_state.db:
        st.session_state.searches += 1
        with st.spinner("🔄 Scanning vector space..."):
            time.sleep(0.5)  # Dramatic pause
            matches = st.session_state.db.similarity_search_with_relevance_scores(query, k=top_k)
        
        st.markdown("### <span class='neon-text'>🎯 TOP MATCHES</span>", unsafe_allow_html=True)
        
        for i, (doc, score) in enumerate(matches, 1):
            st.markdown(f"""
            <div class="result-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                    <span class="result-header">ALPHA-{i}</span>
                    <span class="score-badge">MATCH {score:.1%}</span>
                </div>
                <div style="color: #e0e0ff; line-height: 1.8; font-size: 1.1rem;">
                    {doc.page_content[:800]}{'...' if len(doc.page_content) > 800 else ''}
                </div>
            </div>
            """, unsafe_allow_html=True)
    elif query:
        st.error("🚫 No documents indexed. Upload files in INGEST tab first.")

# --- TAB 2: INGEST ---
with tab2:
    st.markdown("### 📤 <span class='neon-text'>DOCUMENT INGESTION</span>", unsafe_allow_html=True)
    
    files = st.file_uploader("Choose files", 
                           type=['pdf', 'docx', 'txt'], 
                           accept_multiple_files=True,
                           help="Supports PDF, DOCX, TXT")
    
    col1, col2 = st.columns(2)
    with col1:
        chunk_size = st.number_input("Chunk Size", 500, 3000, 1200, help="Text segment length")
    with col2:
        overlap = st.number_input("Overlap", 0, 500, 150, help="Chunk overlap for context")
    
    if st.button("🚀 START HYPER-INDEXING", type="primary", key="index", help="Process all files"):
        if files:
            with st.spinner("🔬 Analyzing semantic structure..."):
                chunks = process_data(files, chunk_size, overlap)
                embeds = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
                st.session_state.db = FAISS.from_documents(chunks, embeds)
                st.session_state.docs = len(files)
                st.session_state.chunks = len(chunks)
                st.session_state.status = "🟢 ACTIVE"
            st.balloons()
            st.success("✅ HYPER-INDEXING COMPLETE!")
        else:
            st.warning("📎 Please upload files first")

# --- TAB 3: METRICS ---
with tab3:
    st.markdown("### 📊 <span class='neon-text'>REAL-TIME ANALYTICS</span>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <h3 style="color: #a0a0ff; margin-bottom: 1rem;">📁 DOCUMENTS</h3>
            <div class="stat-number">{st.session_state.docs}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <h3 style="color: #a0a0ff; margin-bottom: 1rem;">🔹 SEGMENTS</h3>
            <div class="stat-number">{st.session_state.chunks:,}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <h3 style="color: #a0a0ff; margin-bottom: 1rem;">⚡ QUERIES</h3>
            <div class="stat-number">{st.session_state.searches}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"**Status:** {st.session_state.status}")

# --- TAB 4: CONTROL PANEL ---
with tab4:
    st.markdown("""
    <div style="background: rgba(17,17,17,0.9); padding: 3rem; border-radius: 25px; border: 2px solid rgba(0,242,254,0.3); backdrop-filter: blur(20px);">
        <h2 class="neon-text" style="text-align: center; margin-bottom: 2rem;">🧠 ARCHITECTURE</h2>
        <div style="color: #e0e0ff; line-height: 2; font-size: 1.1rem;">
            <p><b>🚀 CORE ENGINE:</b> FAISS Vector Database + HuggingFace Embeddings</p>
            <p><b>⚡ SPEED:</b> Sub-millisecond similarity search</p>
            <p><b>🧮 MODEL:</b> all-MiniLM-L6-v2 (384 dimensions)</p>
            <p><b>🎯 TECH:</b> Semantic chunking + cosine similarity</p>
            <hr style="border-color: rgba(0,242,254,0.3);">
            <p style="text-align: center; color: #00f2fe; font-weight: 900;">
                BUILT FOR SPEED • SCALED FOR ENTERPRISE • DESIGNED FOR AI
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("""
<div style="
    text-align: center; 
    padding: 3rem; 
    color: #888; 
    border-top: 1px solid rgba(0,242,254,0.2);
    margin-top: 3rem;
">
    <p><span class="neon-text" style="font-size: 1.5rem;">NEOSEARCH AI</span> | Powered by Vector Intelligence</p>
</div>
""", unsafe_allow_html=True)