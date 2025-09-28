# 📰 DAILY TECH NEWS AGENT

An **AI-powered agent** that fetches the **latest weekly tech news**, generates a **professional digest** using Google Gemini LLM, and can **send the news directly to WhatsApp**.  

<img width="1221" height="618" alt="top ai news" src="https://github.com/user-attachments/assets/411cd290-1bd2-485d-be90-ca2abb37bb9c" />

Built with **Streamlit**, **LangChain**, **Tavily Search**, and **PyWhatKit**.  

---

## 🚀 Features
- 🔎 Fetches **latest tech news** (AI, startups, big tech, cybersecurity, product launches, etc.)
- 🧠 Summarizes news with **Google Gemini (LLM)** into clear, structured digests
- 🎨 Clean, modern **Streamlit UI** with custom styles
- 📤 Option to **send summarized news to WhatsApp** instantly

---

## ⚙️ Requirements
- Python 3.9+
- Streamlit
- LangChain + Google Generative AI
- Tavily Search API
- PyWhatKit
- dotenv

---

## 🔑 Setup

1. **Clone this repo**
   ```bash
   git clone https://github.com/HAMzAliKj/DAILY-TECH-NEWS-AGENT-.git
   cd DAILY-TECH-NEWS-AGENT-

Install dependencies


pip install -r requirements.txt


Setup environment variables

Create a .env file in the project root (you can copy .env.example).

Add your API keys and WhatsApp number:

TAVILY_API_KEY=your_tavily_api_key
GOOGLE_API_KEY=your_google_gemini_api_key
WHATSAPP_NUMBER=+" "

▶️ Run the App
streamlit run app.py
