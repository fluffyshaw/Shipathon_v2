import streamlit as st
import joblib
import os

# Page configuration
st.set_page_config(
    page_title="Lyrics Genre Predictor",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern, premium design
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        background: #0f0f1e;
        padding: 0;
    }
    
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    /* Hero Section */
    .hero-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 4rem 2rem;
        text-align: center;
        border-radius: 0 0 50px 50px;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
        margin-bottom: 3rem;
        position: relative;
        overflow: hidden;
    }
    
    .hero-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
        background-size: 50px 50px;
        animation: moveBackground 20s linear infinite;
    }
    
    @keyframes moveBackground {
        0% { transform: translate(0, 0); }
        100% { transform: translate(50px, 50px); }
    }
    
    .hero-title {
        font-size: 4rem;
        font-weight: 800;
        color: white;
        margin-bottom: 0.5rem;
        text-shadow: 0 4px 20px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    .hero-group {
        font-size: 1.1rem;
        color: rgba(255,255,255,0.8);
        font-weight: 500;
        margin-bottom: 1rem;
        position: relative;
        z-index: 1;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        color: rgba(255,255,255,0.9);
        font-weight: 400;
        position: relative;
        z-index: 1;
    }
    
    .hero-emoji {
        font-size: 5rem;
        margin-bottom: 1rem;
        display: block;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    
    /* Cards */
    .prediction-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 3rem;
        border-radius: 24px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        margin-bottom: 2rem;
    }
    
    .result-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(102, 126, 234, 0.3);
        padding: 2rem;
        border-radius: 20px;
        margin-top: 2rem;
    }
    
    /* Text Area */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 2px solid rgba(102, 126, 234, 0.3) !important;
        border-radius: 16px !important;
        color: white !important;
        font-size: 1.1rem !important;
        padding: 1.5rem !important;
        min-height: 300px !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stTextArea label {
        color: white !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        margin-bottom: 1rem !important;
    }
    
    /* Button */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        padding: 1.2rem 3rem !important;
        border-radius: 50px !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: all 0.3s ease !important;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6) !important;
    }
    
    /* Genre Result */
    .genre-result {
        text-align: center;
        padding: 3rem;
        margin: 2rem 0;
    }
    
    .genre-badge {
        display: inline-block;
        padding: 1.5rem 4rem;
        border-radius: 100px;
        font-size: 3rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 3px;
        box-shadow: 0 15px 50px rgba(0,0,0,0.4);
        animation: popIn 0.5s ease;
    }
    
    @keyframes popIn {
        0% { transform: scale(0); opacity: 0; }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); opacity: 1; }
    }
    
    /* Confidence Bars */
    .confidence-item {
        margin: 1.5rem 0;
    }
    
    .confidence-header {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.5rem;
    }
    
    .genre-name {
        font-size: 1.1rem;
        font-weight: 600;
        color: white;
    }
    
    .confidence-value {
        font-size: 1.1rem;
        font-weight: 700;
        color: #667eea;
    }
    
    .confidence-bar-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50px;
        height: 20px;
        overflow: hidden;
        position: relative;
    }
    
    .confidence-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 50px;
        transition: width 1s ease;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Section Headers */
    .section-header {
        color: white;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    /* Features Grid */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 2rem;
        margin: 3rem 0;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        border-color: #667eea;
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        color: white;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        color: rgba(255,255,255,0.7);
        font-size: 0.95rem;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 4rem;
        color: rgba(255,255,255,0.5);
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)

# Load models at startup
@st.cache_resource
def load_models():
    try:
        model = joblib.load('model.pkl')
        vectorizer = joblib.load('vectorizer.pkl')
        label_encoder = joblib.load('label_encoder.pkl')
        return model, vectorizer, label_encoder, True
    except Exception as e:
        return None, None, None, False

model, vectorizer, label_encoder, models_loaded = load_models()

# Hero Section
st.markdown("""
    <div class="hero-container">
        <span class="hero-emoji">🎵</span>
        <h1 class="hero-title">Lyrics Genre Predictor</h1>
        <p class="hero-group">By Synaptic Quads</p>
        <p class="hero-subtitle">Powered by AI • Discover the soul of your music through intelligent text analysis</p>
    </div>
""", unsafe_allow_html=True)

if not models_loaded:
    st.error("⚠️ Models not found! Please make sure model.pkl, vectorizer.pkl, and label_encoder.pkl are in the same folder.")
else:
    # Features Section
    st.markdown("""
        <div class="features-grid">
            <div class="feature-card">
                <div class="feature-icon">🚀</div>
                <div class="feature-title">Lightning Fast</div>
                <div class="feature-desc">Get instant predictions in milliseconds</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🎯</div>
                <div class="feature-title">Highly Accurate</div>
                <div class="feature-desc">65%+ accuracy on diverse music genres</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🧠</div>
                <div class="feature-title">AI-Powered</div>
                <div class="feature-desc">Advanced machine learning algorithm</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Main Prediction Section
    st.markdown('<div class="prediction-card">', unsafe_allow_html=True)
    
    lyrics_input = st.text_area(
        "🎤 Enter Your Song Lyrics",
        height=300,
        placeholder="Paste your song lyrics here...\n\nExample:\n\nI see trees of green, red roses too\nI see them bloom for me and you\nAnd I think to myself, what a wonderful world\n\nI see skies of blue and clouds of white\nThe bright blessed day, the dark sacred night\nAnd I think to myself, what a wonderful world...",
        key="lyrics"
    )
    
    if st.button("🔮 Predict Genre", type="primary"):
        if lyrics_input.strip():
            with st.spinner("🎵 Analyzing lyrics..."):
                try:
                    # Transform and predict
                    lyrics_vectorized = vectorizer.transform([lyrics_input])
                    prediction = model.predict(lyrics_vectorized)
                    predicted_genre = label_encoder.inverse_transform(prediction)[0]
                    probs = model.predict_proba(lyrics_vectorized)[0]
                    
                    # Genre colors mapping
                    genre_colors = {
                        'Rock': 'linear-gradient(135deg, #e74c3c 0%, #c0392b 100%)',
                        'Pop': 'linear-gradient(135deg, #3498db 0%, #2980b9 100%)',
                        'Hip-Hop': 'linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%)',
                        'Country': 'linear-gradient(135deg, #f39c12 0%, #e67e22 100%)',
                        'Jazz': 'linear-gradient(135deg, #1abc9c 0%, #16a085 100%)',
                        'Blues': 'linear-gradient(135deg, #34495e 0%, #2c3e50 100%)',
                        'Electronic': 'linear-gradient(135deg, #e67e22 0%, #d35400 100%)',
                        'Classical': 'linear-gradient(135deg, #95a5a6 0%, #7f8c8d 100%)',
                        'R&B': 'linear-gradient(135deg, #c0392b 0%, #a93226 100%)',
                        'Metal': 'linear-gradient(135deg, #7f8c8d 0%, #34495e 100%)'
                    }
                    
                    gradient = genre_colors.get(predicted_genre, 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)')
                    
                    # Display Result
                    st.markdown('<div class="result-card">', unsafe_allow_html=True)
                    
                    st.markdown(f"""
                        <div class="genre-result">
                            <div class="genre-badge" style="background: {gradient}; color: white;">
                                {predicted_genre}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Confidence Levels
                    st.markdown('<div class="section-header">📊 Confidence Analysis</div>', unsafe_allow_html=True)
                    
                    genre_names = label_encoder.classes_
                    sorted_indices = probs.argsort()[::-1]
                    
                    for idx in sorted_indices:
                        genre = genre_names[idx]
                        confidence = probs[idx] * 100
                        
                        st.markdown(f"""
                            <div class="confidence-item">
                                <div class="confidence-header">
                                    <span class="genre-name">{genre}</span>
                                    <span class="confidence-value">{confidence:.1f}%</span>
                                </div>
                                <div class="confidence-bar-container">
                                    <div class="confidence-bar-fill" style="width: {confidence}%;"></div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Success message
                    st.success("✨ Prediction complete! The AI has analyzed your lyrics.")
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("⚠️ Please enter some lyrics to analyze!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        Built with ❤️ by Synaptic Quads using Streamlit & Machine Learning | © 2026 Lyrics Genre Predictor
    </div>
""", unsafe_allow_html=True)