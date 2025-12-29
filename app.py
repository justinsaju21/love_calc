import streamlit as st
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="💘 Love Calc 3000 💘", page_icon="💘", layout="centered")

# --- MEGA CSS FOR CHEESY 2000s + MODERN POLISH ---
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Pacifico&family=Poppins:wght@400;600;700;900&display=swap" rel="stylesheet">
<style>
    /* ===== VARIABLES ===== */
    :root {
        --hot-pink: #FF1493;
        --soft-pink: #FF69B4;
        --deep-red: #C70039;
        --light-pink: #FFB6C1;
        --cream: #FFF0F5;
        --text-shadow: 0 1px 2px rgba(255,255,255,0.8), 0 0 10px rgba(255,255,255,0.4);
    }

    /* ===== HIDE STREAMLIT DEFAULTS ===== */
    #MainMenu, header, footer, [data-testid="stToolbar"] {
        visibility: hidden !important;
        display: none !important;
    }

    /* ===== ANIMATED GRADIENT BACKGROUND ===== */
    .stApp {
        background: linear-gradient(-45deg, #FF9A9E, #FECFEF, #FFB6C1, #FF69B4, #FECFEF);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* ===== FLOATING HEARTS BACKGROUND ===== */
    .stApp::before {
        content: "💕";
        position: fixed;
        top: 10%;
        left: 5%;
        font-size: 3rem;
        opacity: 0.3;
        animation: float 6s ease-in-out infinite;
        pointer-events: none;
    }
    .stApp::after {
        content: "💖";
        position: fixed;
        top: 20%;
        right: 8%;
        font-size: 2.5rem;
        opacity: 0.25;
        animation: float 8s ease-in-out infinite reverse;
        pointer-events: none;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0) rotate(-5deg); }
        50% { transform: translateY(-20px) rotate(5deg); }
    }

    /* ===== GLASSMORPHISM CARD ===== */
    [data-testid="stAppViewContainer"] > .main > .block-container {
        max-width: 520px !important;
        padding: 2.5rem 2rem !important;
        background: rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border-radius: 30px !important;
        border: 3px solid rgba(255, 255, 255, 0.6) !important;
        box-shadow: 
            0 8px 32px rgba(255, 20, 147, 0.2),
            0 0 0 1px rgba(255, 255, 255, 0.5),
            inset 0 0 20px rgba(255, 255, 255, 0.3) !important;
        margin: 8vh auto !important;
        position: relative;
    }

    /* ===== TITLE STYLING (with text shadow for contrast) ===== */
    .main-title {
        font-family: 'Pacifico', cursive !important;
        font-size: 3.8rem !important;
        color: var(--deep-red) !important;
        text-align: center;
        margin-bottom: 0.2rem;
        line-height: 1.2;
        text-shadow: 
            2px 2px 0px rgba(255, 255, 255, 0.9),
            -1px -1px 0px rgba(255, 255, 255, 0.9),
            0 0 20px rgba(255, 255, 255, 0.5);
    }
    
    .subtitle {
        font-family: 'Poppins', sans-serif;
        color: var(--deep-red);
        font-size: 1.1rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2rem;
        letter-spacing: 0.5px;
        text-shadow: var(--text-shadow);
    }

    /* ===== DECORATIVE HEARTS ROW ===== */
    .hearts-row {
        text-align: center;
        font-size: 1.8rem;
        margin-bottom: 1.5rem;
        letter-spacing: 8px;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }

    /* ===== INPUT STYLING ===== */
    [data-testid="stTextInput"] {
        margin-bottom: 0.8rem;
    }
    
    [data-testid="stTextInput"] label {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        color: var(--deep-red) !important;
        margin-bottom: 0.3rem !important;
        text-shadow: var(--text-shadow);
    }
    
    [data-testid="stTextInput"] input {
        font-family: 'Poppins', sans-serif !important;
        font-size: 1rem !important;
        padding: 0.8rem 1rem !important;
        border: 2px solid var(--light-pink) !important;
        border-radius: 15px !important;
        background: rgba(255, 255, 255, 0.95) !important;
        color: #333 !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stTextInput"] input:focus {
        border-color: var(--hot-pink) !important;
        box-shadow: 0 0 0 3px rgba(255, 20, 147, 0.15), 0 4px 12px rgba(255, 20, 147, 0.2) !important;
        background: white !important;
    }
    
    [data-testid="stTextInput"] input::placeholder {
        color: #bbb !important;
        font-style: italic;
    }

    /* ===== BUTTON CONTAINER - CENTERED ===== */
    [data-testid="stHorizontalBlock"] {
        justify-content: center !important;
    }
    
    .stButton {
        margin-top: 1rem;
        display: flex !important;
        justify-content: center !important;
    }
    
    .stButton > button {
        width: 100% !important;
        font-family: 'Poppins', sans-serif !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        padding: 0.9rem 2rem !important;
        background: linear-gradient(135deg, var(--hot-pink), var(--deep-red)) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        box-shadow: 0 6px 20px rgba(199, 0, 57, 0.4) !important;
        cursor: pointer !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative;
        overflow: hidden;
        text-shadow: 0 1px 2px rgba(0,0,0,0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 10px 30px rgba(199, 0, 57, 0.5) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) scale(0.98) !important;
    }

    /* ===== RESULTS STYLING ===== */
    .result-container {
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(255,240,245,0.95));
        border-radius: 20px;
        border: 2px solid rgba(255, 182, 193, 0.5);
        margin-top: 1.5rem;
        animation: popIn 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    }
    
    @keyframes popIn {
        0% { opacity: 0; transform: scale(0.5); }
        100% { opacity: 1; transform: scale(1); }
    }
    
    .result-score {
        font-family: 'Poppins', sans-serif;
        font-size: 5rem;
        font-weight: 900;
        color: var(--deep-red);
        line-height: 1;
        margin: 0.5rem 0;
        text-shadow: 2px 2px 0px rgba(255,255,255,0.8);
    }
    
    .result-message {
        font-family: 'Poppins', sans-serif;
        font-size: 1.3rem;
        color: #444;
        font-weight: 600;
        margin-top: 0.5rem;
        padding: 0.8rem;
        background: rgba(255, 255, 255, 0.7);
        border-radius: 12px;
    }

    /* ===== LOADING ANIMATION ===== */
    .loading-container {
        text-align: center;
        padding: 2rem;
    }
    
    .heart-throb {
        font-size: 5rem;
        display: inline-block;
        animation: heartbeat 0.6s ease-in-out infinite;
    }
    
    @keyframes heartbeat {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.3); }
    }
    
    .loading-text {
        font-family: 'Poppins', sans-serif;
        color: var(--deep-red);
        font-size: 1.1rem;
        font-weight: 700;
        margin-top: 1rem;
        animation: blink 1s ease-in-out infinite;
        text-shadow: var(--text-shadow);
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* ===== FOOTER CREDIT ===== */
    .footer-credit {
        text-align: center;
        font-family: 'Poppins', sans-serif;
        font-size: 0.75rem;
        color: var(--deep-red);
        margin-top: 2rem;
        letter-spacing: 1px;
        opacity: 0.7;
        text-shadow: var(--text-shadow);
    }

</style>
""", unsafe_allow_html=True)


# --- LOGIC ---
def calculate_love_score(name1, name2):
    if not name1 or not name2:
        return 0
    clean1 = name1.lower().strip()
    clean2 = name2.lower().strip()
    sum1 = sum(ord(c) for c in clean1)
    sum2 = sum(ord(c) for c in clean2)
    return (sum1 + sum2) % 101

def get_commentary(percentage):
    if percentage == 0: return "Absolute zero. It's physically impossible. 🥶"
    if percentage <= 10: return "Restraining order recommended. 🚨"
    if percentage <= 20: return "Maybe in another universe. 🌌"
    if percentage <= 30: return "It's a no from me, dawg. 🙅"
    if percentage <= 40: return "I mean... if you're both desperate. 😬"
    if percentage <= 50: return "Friend zone territory. 🤝"
    if percentage <= 60: return "Safe bet. Boring, but safe. 😐"
    if percentage <= 68: return "Getting spicy... 🌶️"
    if percentage == 69: return "Nice. 😏"
    if percentage <= 79: return "Pretty solid match! 💪"
    if percentage <= 89: return "Relationship goals! 💑"
    if percentage <= 99: return "Start naming your children! 👶"
    if percentage == 100: return "ERROR: Too much love. System overheating! 🔥💥"
    return "Unknown destiny... 🔮"


def send_notification_email(name1, name2, score):
    """Send email notification with the love calculation results."""
    try:
        # Read credentials from Streamlit secrets
        # Support both [email] section and flat format
        email_sec = st.secrets.get("email", {})
        sender_email = email_sec.get("username", st.secrets.get("SENDER_EMAIL"))
        app_password = email_sec.get("password", st.secrets.get("APP_PASSWORD"))
        
        smtp_server = email_sec.get("smtp_server", st.secrets.get("SMTP_SERVER", "smtp.gmail.com"))
        smtp_port = email_sec.get("smtp_port", st.secrets.get("SMTP_PORT", 587))
        recipient_email = "justinsaju100@gmail.com"
        
        if not sender_email or not app_password:
            return False
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"💘 Love Calc 3000 - New Calculation!"
        
        # Email body
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        body = f"""
        💕 New Love Calculation Alert! 💕
        
        Names: {name1} ❤️ {name2}
        Score: {score}%
        Time: {timestamp}
        
        ---
        Sent from Love Calc 3000
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, app_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        
        return True
    except Exception as e:
        # Silently fail - don't break the app if email fails
        return False


# --- UI LAYOUT ---

# Title with shimmer effect
st.markdown('<h1 class="main-title">Love Calc 3000</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">✨ Is it destiny or disaster? ✨</p>', unsafe_allow_html=True)

# Decorative hearts
st.markdown('<div class="hearts-row">💕 💖 💕</div>', unsafe_allow_html=True)

# Input columns
col1, col2 = st.columns(2)

with col1:
    name1 = st.text_input("💗 First Name", placeholder="Romeo")

with col2:
    name2 = st.text_input("💗 Second Name", placeholder="Juliet")

# Calculate button - centered using columns
_, btn_col, _ = st.columns([1, 2, 1])
with btn_col:
    calculate_btn = st.button("💘 Calculate Love! 💘", use_container_width=True)

if calculate_btn:
    if not name1 or not name2:
        st.error("💔 Please enter both names! Love needs two people!")
    else:
        # Show loading animation
        placeholder = st.empty()
        with placeholder.container():
            st.markdown("""
            <div class="loading-container">
                <div class="heart-throb">❤️</div>
                <div class="loading-text">Analyzing cosmic love energy...</div>
            </div>
            """, unsafe_allow_html=True)
        
        time.sleep(2)  # Dramatic pause
        
        # Calculate and show result
        score = calculate_love_score(name1, name2)
        message = get_commentary(score)
        
        # Send email notification (runs silently in background)
        send_notification_email(name1, name2, score)
        
        placeholder.empty()
        
        st.markdown(f"""
        <div class="result-container">
            <div class="result-score">{score}%</div>
            <div class="result-message">{message}</div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown('<div class="footer-credit">Made with 💖 in the spirit of 2000s internet</div>', unsafe_allow_html=True)
