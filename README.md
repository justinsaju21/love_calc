# Love Calc 3000 💘

A cheesy 2000s-style Love Calculator web app built with Streamlit.

## Features
- 💕 Deterministic love score algorithm (same names = same result every time)
- 🎨 Animated gradient background with floating hearts
- ✨ Glassmorphism UI with modern polish
- 💌 Email notifications for each calculation (optional)
- 😂 Funny commentary based on the score

## Live Demo
[Try it on Streamlit Cloud](https://lovecalc3000.streamlit.app) *(update with your actual URL)*

## Run Locally
```bash
pip install streamlit
streamlit run app.py
```

## Email Notifications (Optional)
To receive email notifications for each calculation, add these secrets in Streamlit Cloud:

```toml
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your-email@gmail.com"
APP_PASSWORD = "your-16-char-app-password"
```

## Tech Stack
- Python + Streamlit
- Custom CSS animations
- SMTP for email

---
Made with 💖 in the spirit of 2000s internet
