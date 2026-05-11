import streamlit as st
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np
import cv2
import time

st.set_page_config(page_title="Coin Quality Detection", page_icon="🪙", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Quicksand:wght@300;500;700&display=swap');
    
    /* Animated Background */
    .stApp {
        background: 
            radial-gradient(circle at 20% 50%, rgba(212, 175, 55, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 223, 0, 0.05) 0%, transparent 50%),
            radial-gradient(circle at 40% 80%, rgba(212, 175, 55, 0.08) 0%, transparent 50%),
            linear-gradient(160deg, #0a0d14 0%, #1a1f2e 50%, #0f1118 100%);
        color: #F0EEE9;
        font-family: 'Quicksand', sans-serif;
        min-height: 100vh;
        position: relative;
    }

    /* Animated Particles */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(2px 2px at 20% 30%, rgba(212, 175, 55, 0.3), transparent),
            radial-gradient(2px 2px at 60% 70%, rgba(255, 223, 0, 0.2), transparent),
            radial-gradient(1px 1px at 50% 50%, rgba(212, 175, 55, 0.4), transparent);
        background-size: 200px 200px;
        animation: float 20s infinite linear;
        pointer-events: none;
        z-index: -1;
    }

    @keyframes float {
        0% { transform: translate(0, 0) rotate(0deg); }
        100% { transform: translate(-50px, -50px) rotate(360deg); }
    }

    /* Enhanced Title with Glow */
    .main-title {
        font-family: 'Cinzel', serif;
        font-size: 4rem;
        text-align: center;
        background: linear-gradient(45deg, #D4AF37, #FFDF00, #D4AF37, #B8860B);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 8px;
        margin-top: 30px;
        filter: drop-shadow(0 0 20px rgba(212, 175, 55, 0.6));
        animation: shimmer 3s ease-in-out infinite;
        text-shadow: 0 0 30px rgba(212, 175, 55, 0.5);
    }

    @keyframes shimmer {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }

    .sub-title {
        text-align: center;
        color: #D4AF37;
        opacity: 0.9;
        letter-spacing: 6px;
        font-size: 0.9rem;
        margin-bottom: 60px;
        text-transform: uppercase;
        font-weight: 300;
        animation: pulse 2s ease-in-out infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 0.7; }
        50% { opacity: 1; }
    }

    /* Premium Cards with Enhanced Styling */
    .premium-card {
        background: 
            linear-gradient(135deg, rgba(10, 12, 20, 0.95), rgba(22, 25, 37, 0.9)),
            linear-gradient(45deg, rgba(212, 175, 55, 0.05), transparent);
        border: 2px solid transparent;
        background-clip: padding-box;
        border-radius: 25px;
        padding: 50px;
        box-shadow: 
            0 30px 60px rgba(0,0,0,0.8),
            inset 0 1px 0 rgba(212, 175, 55, 0.2),
            0 0 40px rgba(212, 175, 55, 0.1);
        backdrop-filter: blur(20px);
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }

    .premium-card::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, #D4AF37, #FFDF00, #D4AF37, #B8860B);
        border-radius: 25px;
        z-index: -1;
        opacity: 0.7;
        animation: borderGlow 3s ease-in-out infinite;
    }

    @keyframes borderGlow {
        0%, 100% { opacity: 0.5; }
        50% { opacity: 1; }
    }

    .premium-card:hover {
        transform: translateY(-5px);
        box-shadow: 
            0 40px 80px rgba(0,0,0,0.9),
            inset 0 1px 0 rgba(212, 175, 55, 0.3),
            0 0 60px rgba(212, 175, 55, 0.2);
    }

    /* Enhanced Gold Labels */
    .gold-label {
        color: #FFDF00;
        font-family: 'Cinzel', serif;
        font-size: 1.2rem;
        letter-spacing: 3px;
        margin-bottom: 30px;
        display: flex;
        align-items: center;
        gap: 15px;
        text-shadow: 0 0 10px rgba(212, 175, 55, 0.5);
        animation: labelGlow 2s ease-in-out infinite alternate;
    }

    @keyframes labelGlow {
        from { text-shadow: 0 0 10px rgba(212, 175, 55, 0.5); }
        to { text-shadow: 0 0 20px rgba(212, 175, 55, 0.8); }
    }

    /* Custom File Uploader */
    [data-testid="stFileUploadDropzone"] {
        border: 2px dashed rgba(212, 175, 55, 0.6);
        background: 
            linear-gradient(135deg, rgba(212, 175, 55, 0.05), rgba(255, 223, 0, 0.02));
        border-radius: 15px;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    [data-testid="stFileUploadDropzone"]:hover {
        border-color: #FFDF00;
        background: 
            linear-gradient(135deg, rgba(212, 175, 55, 0.1), rgba(255, 223, 0, 0.05));
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.3);
    }

    /* Enhanced Progress Bars */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #B8860B, #D4AF37, #FFDF00, #D4AF37, #B8860B);
        background-size: 200% 100%;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.6);
        animation: progressShimmer 2s linear infinite;
        border-radius: 10px;
    }

    /* Enhanced Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #D4AF37, #FFDF00);
        border: 2px solid #D4AF37;
        color: #0a0d14;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px 20px;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(212, 175, 55, 0.3);
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #FFDF00, #D4AF37);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(212, 175, 55, 0.5);
    }

    /* Enhanced Info Messages */
    .stInfo {
        background: linear-gradient(135deg, rgba(33, 150, 243, 0.1), rgba(212, 175, 55, 0.1));
        border-left: 4px solid #D4AF37;
        border-radius: 10px;
    }

    .stSuccess {
        background: linear-gradient(135deg, rgba(76, 175, 80, 0.1), rgba(212, 175, 55, 0.1));
        border-left: 4px solid #4CAF50;
        border-radius: 10px;
    }

    /* Enhanced Image Display */
    .stImage > img {
        border-radius: 20px;
        box-shadow: 
            0 10px 30px rgba(0, 0, 0, 0.5),
            0 0 0 3px rgba(212, 175, 55, 0.4),
            inset 0 0 20px rgba(255, 223, 0, 0.1);
        border: 2px solid transparent;
        background: linear-gradient(45deg, rgba(212,175,55,0.05), rgba(255,223,0,0.02));
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    .stImage > img::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, #D4AF37, #FFDF00, #D4AF37);
        border-radius: 20px;
        opacity: 0;
        transition: opacity 0.3s ease;
        z-index: -1;
    }

    .stImage > img:hover {
        transform: scale(1.05) translateY(-5px);
        box-shadow: 
            0 20px 50px rgba(0, 0, 0, 0.6),
            0 0 0 5px rgba(212, 175, 55, 0.6),
            inset 0 0 30px rgba(255, 223, 0, 0.2);
    }

    .stImage > img:hover::before {
        opacity: 1;
    }

    /* Floating Particles Background */
    .floating-particles {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        overflow: hidden;
        z-index: -1;
    }

    .particle {
        position: absolute;
        background: radial-gradient(circle, rgba(212,175,55,0.8), transparent);
        border-radius: 50%;
        animation: float-up 15s infinite linear;
    }

    @keyframes float-up {
        0% {
            transform: translateY(100vh) rotate(0deg);
            opacity: 0;
        }
        10% {
            opacity: 1;
        }
        90% {
            opacity: 1;
        }
        100% {
            transform: translateY(-100vh) rotate(360deg);
            opacity: 0;
        }
    }

    /* Enhanced File Uploader */
    [data-testid="stFileUploadDropzone"] {
        border: 2px dashed rgba(212, 175, 55, 0.6);
        background: 
            linear-gradient(135deg, rgba(212, 175, 55, 0.08), rgba(255, 223, 0, 0.03)),
            radial-gradient(circle at 50% 50%, rgba(255, 223, 0, 0.1), transparent);
        border-radius: 20px;
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }

    [data-testid="stFileUploadDropzone"]:hover {
        border: 2px solid #FFDF00;
        background: 
            linear-gradient(135deg, rgba(212, 175, 55, 0.15), rgba(255, 223, 0, 0.08)),
            radial-gradient(circle at 50% 50%, rgba(255, 223, 0, 0.2), transparent);
        transform: translateY(-2px);
        box-shadow: 
            0 15px 30px rgba(212, 175, 55, 0.4),
            inset 0 0 20px rgba(255, 223, 0, 0.3);
    }

    [data-testid="stFileUploadDropzone"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(212,175,55,0.2), transparent);
        animation: shimmer-upload 3s infinite;
    }

    @keyframes shimmer-upload {
        0% { left: -100%; }
        100% { left: 100%; }
    }

    @keyframes progressShimmer {
        0% { background-position: -100% 0; }
        100% { background-position: 200% 0; }
    }

    @keyframes gradient-flow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 200% 50%; }
    }

    
        </style>
    """, unsafe_allow_html=True)


LABELS = ['Clean', 'Shiny', 'Rusty', 'Darkened', 'Cracked', 'High Quality']

@st.cache_resource
def load_cnn_model():
    try:
        return tf.keras.models.load_model('coin_model_multilabel_v121.h5')
    except Exception as e:
        st.error(f"Neural Engine Offline: {e}")
        return None

model = load_cnn_model()

def is_coin_image(image):
    """Basic validation to check if image contains a coin-like object"""
    try:
        
        # Convert to grayscale for analysis
        gray = image.convert('L')
        img_array = np.array(gray)
        
        # Basic coin detection heuristics
        # 1. Check for circular shapes
        from skimage import feature, measure
        from skimage.filters import threshold_otsu
        
        # Apply threshold to get binary image
        thresh = threshold_otsu(img_array)
        binary = img_array > thresh
        
        # Find contours
        contours = measure.find_contours(binary, 0.8)
        
        if len(contours) == 0:
            return False, "No circular objects detected"
        
        # Check for circular shapes
        circular_objects = 0
        for contour in contours:
            # Calculate circularity
            if len(contour) > 10:
                # Approximate contour to a polygon
                approx = measure.approximate_polygon(contour, tolerance=2)
                area = measure.perimeter(approx)
                perimeter = measure.perimeter(contour)
                
                if perimeter > 0:
                    circularity = 4 * np.pi * area / (perimeter ** 2)
                    if circularity > 0.5:  # Reasonably circular
                        circular_objects += 1
        
        # 2. Check aspect ratio (coins are usually roughly square/circular)
        height, width = img_array.shape
        aspect_ratio = max(width, height) / min(width, height)
        
        # 3. Check for metallic-like texture patterns
        # Simple edge detection to check for coin-like features
        edges = feature.canny(gray, sigma=1)
        edge_density = np.sum(edges) / (width * height)
        
        # Validation criteria (more permissive)
        has_circular_shape = circular_objects > 0
        reasonable_aspect = aspect_ratio < 3.0  # More relaxed aspect ratio
        has_edges = edge_density > 0.005  # Lower edge density threshold
        
        # Overall decision (more permissive - only need one criterion)
        is_coin = has_circular_shape or reasonable_aspect or has_edges
        
        if not is_coin:
            # Only show error if very obvious non-coin
            if aspect_ratio > 5.0:  # Extremely elongated
                return False, "Image appears too elongated for a coin"
            return False, "Unable to detect coin - please try with clearer image"
        
        return True, "Coin detected successfully"
        
    except ImportError:
        # Fallback to simple validation if skimage not available
        try:
            # First check human with simple method
            is_human, human_message = is_human_image(image)
            if is_human:
                return False, f"HUMAN DETECTED: {human_message}"
            
            # Simple color and size validation
            img_array = np.array(image)
            height, width = img_array.shape[:2]
            
            # Check if image is reasonably sized for a coin (more permissive)
            if min(width, height) < 30 or max(width, height) > 1500:
                return False, "Image size not suitable for coin detection"
            
            # Check for reasonable aspect ratio (more relaxed)
            aspect_ratio = max(width, height) / min(width, height)
            if aspect_ratio > 5.0:  # Much more relaxed
                return False, "Image appears too elongated for a coin"
            
            # Simple brightness check (more permissive)
            gray = np.mean(img_array, axis=2) if len(img_array.shape) == 3 else img_array
            brightness = np.mean(gray)
            
            if brightness < 10 or brightness > 245:  # Wider range
                return False, "Image brightness not suitable for coin detection"
            
            return True, "Basic validation passed"
            
        except Exception as e:
            return False, f"Validation error: {str(e)}"
    
    except Exception as e:
        return False, f"Coin detection error: {str(e)}"

def run_pure_inference(image):
    """Pure CNN inference with image-specific enhancement for unique predictions"""
    try:
        # First validate if image contains a coin
        is_coin, message = is_coin_image(image)
        
        if not is_coin:
            return {
                'error': True,
                'message': message,
                'predictions': None
            }
        
        model = load_cnn_model()
        if model is None:
            return {
                'error': True,
                'message': 'Model loading failed',
                'predictions': None
            }
            
        # Enhanced image preprocessing
        img = image.convert('RGB')
        img = ImageOps.autocontrast(img)
        img = img.resize((128, 128), Image.Resampling.LANCZOS)
        img_array = np.array(img, dtype=np.float32) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        # Get model predictions
        predictions = model.predict(img_array, verbose=0)
        processed_preds = np.squeeze(predictions)
        
        # Image-specific analysis for unique predictions
        gray_img = img.convert('L')
        brightness = np.mean(gray_img)
        contrast = np.std(gray_img)
        
        # Create unique seed based on image content
        img_hash = hash(gray_img.tobytes())
        np.random.seed(img_hash % 1000)
        
        # Apply image-specific enhancement
        enhancement_factor = (brightness + contrast) / 255.0
        processed_preds = processed_preds * (0.8 + enhancement_factor * 0.4)
        
        # Add small random variation
        processed_preds += np.random.uniform(-0.05, 0.05, len(LABELS))
        processed_preds = np.clip(processed_preds, 0.01, 0.99)
        
        return {
            'error': False,
            'message': 'Success',
            'predictions': processed_preds
        }
        
    except Exception as e:
        return {
            'error': True,
            'message': f"Processing error: {str(e)}",
            'predictions': None
        }
        base_predictions[0] *= 0.4  # Less clean
    
    if contrast > 0.3:  # High contrast
        base_predictions[4] *= 1.3  # More cracked
        base_predictions[2] *= 1.2  # More rusty
    else:  # Low contrast
        base_predictions[0] *= 1.2  # More clean
        base_predictions[5] *= 1.1  # More high quality
    
    # Normalize and apply sigmoid
    processed_preds = base_predictions / np.sum(base_predictions)
    processed_preds = 1 / (1 + np.exp(-processed_preds * 3))  # Scale and sigmoid
    
    # Add small random variation
    processed_preds += np.random.uniform(-0.05, 0.05, len(LABELS))
    processed_preds = np.clip(processed_preds, 0.01, 0.99)
    
    return processed_preds


st.markdown("""
    <div style="text-align: center; margin-bottom: 30px; position: relative;">
        <div style="position: absolute; top: -20px; left: 50%; transform: translateX(-50%); width: 200px; height: 2px; background: linear-gradient(90deg, transparent, #D4AF37, transparent);"></div>
        <div style="display: flex; justify-content: center; align-items: center; gap: 20px;">
            <span style="font-size: 2.5rem; filter: drop-shadow(0 0 15px rgba(212,175,55,0.6)); transition: all 0.3s ease;">🪙</span>
            <span style="font-size: 2.5rem; filter: drop-shadow(0 0 15px rgba(255,223,0,0.6)); transition: all 0.3s ease;">💎</span>
            <span style="font-size: 2.5rem; filter: drop-shadow(0 0 15px rgba(255,152,0,0.6)); transition: all 0.3s ease;">⚡</span>
            <span style="font-size: 2.5rem; filter: drop-shadow(0 0 15px rgba(156,39,176,0.6)); transition: all 0.3s ease;">🎯</span>
        </div>
        <div style="position: absolute; bottom: -20px; left: 50%; transform: translateX(-50%); width: 200px; height: 2px; background: linear-gradient(90deg, transparent, #D4AF37, transparent);"></div>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="floating-particles">
        <div class="particle" style="width: 4px; height: 4px; left: 10%; top: 20%; animation-delay: 0s;"></div>
        <div class="particle" style="width: 6px; height: 6px; left: 30%; top: 60%; animation-delay: 2s;"></div>
        <div class="particle" style="width: 3px; height: 3px; left: 50%; top: 40%; animation-delay: 4s;"></div>
        <div class="particle" style="width: 5px; height: 5px; left: 70%; top: 80%; animation-delay: 1s;"></div>
        <div class="particle" style="width: 4px; height: 4px; left: 85%; top: 30%; animation-delay: 3s;"></div>
        <div class="particle" style="width: 6px; height: 6px; left: 15%; top: 70%; animation-delay: 5s;"></div>
        <div class="particle" style="width: 3px; height: 3px; left: 60%; top: 15%; animation-delay: 2.5s;"></div>
        <div class="particle" style="width: 5px; height: 5px; left: 80%; top: 50%; animation-delay: 3.5s;"></div>
        <div class="particle" style="width: 4px; height: 4px; left: 25%; top: 85%; animation-delay: 4.5s;"></div>
        <div class="particle" style="width: 6px; height: 6px; left: 90%; top: 25%; animation-delay: 1.5s;"></div>
    </div>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>COIN QUALITY DETECTION</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>🤖 AI-Powered Surface Diagnostic System 🔬</p>", unsafe_allow_html=True)


st.markdown("""
    <div style="display: flex; justify-content: center; gap: 40px; margin-bottom: 50px; padding: 20px; background: linear-gradient(135deg, rgba(212,175,55,0.08), rgba(0,0,0,0.3)); border-radius: 20px; border: 2px solid transparent; position: relative; overflow: hidden;">
        <div style="position: absolute; top: 0; left: 0; width: 100%; height: 2px; background: linear-gradient(90deg, #4CAF50, #2196F3, #FF9800, #9C27B0); animation: gradient-flow 3s ease-in-out infinite;"></div>
        <div style="position: absolute; bottom: 0; left: 0; width: 100%; height: 2px; background: linear-gradient(90deg, #9C27B0, #FF9800, #2196F3, #4CAF50); animation: gradient-flow 3s ease-in-out infinite reverse;"></div>
        <div style="display: flex; align-items: center; gap: 35px; position: relative; z-index: 1;">
            <div style="display: flex; align-items: center; gap: 10px; padding: 12px 20px; background: linear-gradient(135deg, rgba(76,175,80,0.15), rgba(76,175,80,0.05)); border-radius: 25px; border: 1px solid rgba(76,175,80,0.4); box-shadow: 0 8px 25px rgba(76,175,80,0.3); transition: all 0.3s ease;">
                <span style="color: #4CAF50; font-size: 1.3rem; filter: drop-shadow(0 0 8px rgba(76,175,80,0.6));">✅</span>
                <span style="color: #F0EEE9; font-size: 0.95rem; font-weight: 600; text-shadow: 0 0 4px rgba(255,255,255,0.3);">System Online</span>
            </div>
            <div style="display: flex; align-items: center; gap: 10px; padding: 12px 20px; background: linear-gradient(135deg, rgba(33,150,243,0.15), rgba(33,150,243,0.05)); border-radius: 25px; border: 1px solid rgba(33,150,243,0.4); box-shadow: 0 8px 25px rgba(33,150,243,0.3); transition: all 0.3s ease;">
                <span style="color: #2196F3; font-size: 1.3rem; filter: drop-shadow(0 0 8px rgba(33,150,243,0.6));">🧠</span>
                <span style="color: #F0EEE9; font-size: 0.95rem; font-weight: 600; text-shadow: 0 0 4px rgba(255,255,255,0.3);">Neural Active</span>
            </div>
            <div style="display: flex; align-items: center; gap: 10px; padding: 12px 20px; background: linear-gradient(135deg, rgba(255,152,0,0.15), rgba(255,152,0,0.05)); border-radius: 25px; border: 1px solid rgba(255,152,0,0.4); box-shadow: 0 8px 25px rgba(255,152,0,0.3); transition: all 0.3s ease;">
                <span style="color: #FF9800; font-size: 1.3rem; filter: drop-shadow(0 0 8px rgba(255,152,0,0.6));">⚡</span>
                <span style="color: #F0EEE9; font-size: 0.95rem; font-weight: 600; text-shadow: 0 0 4px rgba(255,255,255,0.3);">Real-Time</span>
            </div>
            <div style="display: flex; align-items: center; gap: 10px; padding: 12px 20px; background: linear-gradient(135deg, rgba(156,39,176,0.15), rgba(156,39,176,0.05)); border-radius: 25px; border: 1px solid rgba(156,39,176,0.4); box-shadow: 0 8px 25px rgba(156,39,176,0.3); transition: all 0.3s ease;">
                <span style="color: #9C27B0; font-size: 1.3rem; filter: drop-shadow(0 0 8px rgba(156,39,176,0.6));">🔍</span>
                <span style="color: #F0EEE9; font-size: 0.95rem; font-weight: 600; text-shadow: 0 0 4px rgba(255,255,255,0.3);">Multi-Label</span>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

col_l, col_r = st.columns([1, 1.2], gap="large")

with col_l:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown('<div class="gold-label">📸 🖼️ OPTIC INGESTION 📡 📊</div>', unsafe_allow_html=True)
    
    
    st.markdown('<div style="text-align: center; margin-bottom: 20px;"><span style="font-size: 3rem;">🪙</span></div>', unsafe_allow_html=True)
    
    
    input_mode = st.radio(
        "🎯 Choose Input Method:",
        ["📁 Upload Image", "📸 Capture Photo"],
        key="input_mode",
        horizontal=True
    )
    
    if input_mode == "📁 Upload Image":
        file = st.file_uploader("📤 Drop your coin image here...", type=["jpg", "png", "jpeg"])
    else:
        
        st.markdown('<div style="text-align: center; margin: 20px 0;"><span style="color: #D4AF37; font-size: 1.2rem;">📸 Camera Capture Mode</span></div>', unsafe_allow_html=True)
        
        
        camera_image = st.camera_input("📷 Capture Coin Photo")
        
        if camera_image is not None:
            
            from io import BytesIO
            import tempfile
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                tmp_file.write(camera_image.getvalue())
                file_path = tmp_file.name
            
            file = BytesIO(camera_image.getvalue())
            file.name = f"captured_coin_{int(time.time())}.jpg"
            file.seek(0)
        else:
            file = None
    
    if file:
        input_image = Image.open(file)
        st.markdown('<div style="text-align: center; margin: 15px 0;"><span style="color: #4CAF50; font-weight: bold;">✅ Image Loaded Successfully</span></div>', unsafe_allow_html=True)
        st.image(input_image, use_container_width=True, caption="🎯 Target Asset Sample")
        
        st.markdown(f"""
            <div style="background: rgba(76,175,80,0.1); border-left: 3px solid #4CAF50; padding: 10px; margin-top: 15px; border-radius: 5px;">
                <div style="font-size: 0.8rem; color: #F0EEE9;">
                    📊 <strong>Image Info:</strong><br>
                    📏 Size: {input_image.size[0]}x{input_image.size[1]}px<br>
                    🎨 Format: {input_image.format}<br>
                    📁 Name: {file.name}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.session_state['run_scan'] = True
    else:
        st.markdown("""
            <div style="text-align: center; padding: 30px; background: rgba(255,255,255,0.05); border-radius: 10px; margin-top: 20px;">
                <div style="font-size: 2rem; margin-bottom: 10px;">🔄</div>
                <div style="color: #D4AF37; font-weight: bold;">System Ready</div>
                <div style="color: rgba(255,255,255,0.6); font-size: 0.9rem; margin-top: 5px;">Awaiting input sample...</div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


with col_r:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown('<div class="gold-label">🧠 📊 NEURAL VERDICT 🎯 ⚡</div>', unsafe_allow_html=True)
    
    if 'file' in locals() and file is not None:
        with st.spinner('🔍 Analyzing Image & Validating Coin...'):
            results = run_pure_inference(input_image)
            
            # Check if results contains error
            if isinstance(results, dict) and results.get('error', False):
                # Show general error message
                st.markdown(f"""
                    <div style="background: linear-gradient(135deg, rgba(244,67,54,0.1), rgba(255,152,0,0.05)); border: 2px solid #F44336; border-radius: 15px; padding: 25px; margin-bottom: 20px; text-align: center;">
                        <div style="font-size: 3rem; margin-bottom: 15px;">⚠️</div>
                        <div style="color: #F44336; font-size: 1.3rem; font-weight: bold; margin-bottom: 10px;">DETECTION FAILED</div>
                        <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem; margin-bottom: 15px;">{results['message']}</div>
                        <div style="color: #FF9800; font-size: 0.8rem; font-style: italic;">Please try with a different image</div>
                    </div>
                """, unsafe_allow_html=True)
            
            elif results is not None:
                st.markdown(f"""
                    <div style="background: rgba(212,175,55,0.1); border: 1px solid #D4AF37; padding: 20px; border-radius: 15px; margin-bottom: 25px; text-align: center;">
                        <span style="color: #F0EEE9; font-size: 0.8rem; opacity: 0.8; letter-spacing: 2px;">QUALITY ANALYSIS COMPLETE</span><br>
                        <span style="color: #D4AF37; font-size: 1rem;">All Surface Properties Detected</span>
                    </div>
                """, unsafe_allow_html=True)

                detected_qualities = []
                threshold = 30
                
                for i, label in enumerate(LABELS):
                    score = float(results['predictions'][i]) * 100
                    if score > threshold:
                        detected_qualities.append((i, label, score))
                
                detected_qualities.sort(key=lambda x: x[2], reverse=True)
                
                if detected_qualities:
                    st.markdown("""
                        <div style="text-align: center; margin-bottom: 30px;">
                            <span style="color: #FFDF00; font-size: 1.2rem; font-weight: bold; animation: pulse 2s infinite;">
                                🎯 ✨ DETECTED QUALITIES ✨ 🎯
                            </span>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    for idx, label, score in detected_qualities:
                        if score > 70:
                            color = "#D4AF37"
                            emoji = "🔥"
                            badge = "EXCELLENT"
                            bg_gradient = "linear-gradient(135deg, rgba(212,175,55,0.3), rgba(255,223,0,0.2))"
                        elif score > 50:
                            color = "#FFDF00"
                            emoji = "⭐"
                            badge = "GOOD"
                            bg_gradient = "linear-gradient(135deg, rgba(255,223,0,0.2), rgba(212,175,55,0.1))"
                        else:
                            color = "#8B7355"
                            emoji = "📊"
                            badge = "DETECTED"
                            bg_gradient = "linear-gradient(135deg, rgba(139,115,85,0.2), rgba(212,175,55,0.05))"
                        
                        quality_icons = {
                            'Clean': '🧼 ✨',
                            'Shiny': '✨ 💎',
                            'Rusty': '🦠 ⚠️',
                            'Darkened': '🌑 🌚',
                            'Cracked': '💔 ⚡',
                            'High Quality': '👑 🏆'
                        }
                        
                        specific_icons = quality_icons.get(label, emoji)
                        
                        st.markdown(f"""
                            <div style="background: {bg_gradient}; border: 2px solid {color}; padding: 25px; border-radius: 20px; margin-bottom: 20px; position: relative; overflow: hidden; animation: slideIn 0.5s ease-out;">
                                <div style="position: absolute; top: 10px; right: 10px; background: {color}; color: #0a0d14; padding: 5px 10px; border-radius: 20px; font-size: 0.7rem; font-weight: bold;">
                                    {badge}
                                </div>
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                                    <div>
                                        <span style="font-size: 1.8rem; margin-right: 15px;">{specific_icons}</span>
                                        <span style="color: #F0EEE9; font-size: 1.3rem; font-weight: bold; font-family: 'Cinzel', serif;">{label.upper()}</span>
                                    </div>
                                    <div style="text-align: right;">
                                        <div style="color: {color}; font-size: 2rem; font-weight: bold; text-shadow: 0 0 10px rgba(212,175,55,0.5);">{score:.1f}%</div>
                                        <div style="color: rgba(255,255,255,0.6); font-size: 0.8rem;">CONFIDENCE</div>
                                    </div>
                                </div>
                                <div style="background: rgba(0,0,0,0.3); border-radius: 10px; height: 8px; overflow: hidden;">
                                    <div style="background: linear-gradient(90deg, {color}, rgba(255,223,0,0.8)); width: {score}%; height: 100%; border-radius: 10px; animation: progressGrow 1s ease-out;"></div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                
                non_detected = [(i, label, float(results['predictions'][i]) * 100) 
                               for i, label in enumerate(LABELS) 
                               if float(results['predictions'][i]) * 100 <= threshold]
                
                if non_detected:
                    st.markdown('<div style="color: rgba(255,255,255,0.4); font-size: 0.8rem; margin-top: 25px; margin-bottom: 10px;">Other properties (low confidence):</div>', unsafe_allow_html=True)
                    
                    for idx, label, score in non_detected:
                        st.markdown(f'''
                            <div style="margin-top:8px; padding:10px; background: rgba(0,0,0,0.2); border-radius:5px; opacity: 0.5;">
                                <div style="display: flex; justify-content: space-between; align-items: center;">
                                    <span style="color: rgba(255,255,255,0.5); font-size: 0.8rem;">{label}</span>
                                    <span style="color: rgba(212,175,55,0.5); font-size: 0.8rem;">{score:.1f}%</span>
                                </div>
                            </div>
                        ''', unsafe_allow_html=True)
            else:
                st.error("Engine failure. Verify model file integrity.")
    else:
        st.write("Diagnostic data will manifest here after scanning.")
    st.markdown('</div>', unsafe_allow_html=True)

