# %% ------------------------------- UI + Logic (unchanged core) -------------------------------
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch
from langchain.prompts import PromptTemplate  # (kept; not strictly used but you had it)
import os
from dotenv import load_dotenv
import pywhatkit as kit
import asyncio
import time

api_key = "YOUR API KEY"


# ---------- Page & Styles ----------
st.set_page_config(
    page_title="Tech News Summarizer",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="collapsed",
)
if "whatsapp_sent" not in st.session_state:
    st.session_state.whatsapp_sent = False

# Global CSS
st.markdown("""
<style>
/* background */
.stApp {
  background: radial-gradient(1200px 600px at 100% -50%, rgba(56,189,248,0.12), transparent 60%),
              radial-gradient(1200px 600px at -10% 0%, rgba(16,185,129,0.10), transparent 60%),
              linear-gradient(180deg, #0b1220, #0d1324 40%, #0b1220);
  color: #e5e7eb;
}

/* container cards */
.card {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 18px;
  padding: 18px 20px;
  box-shadow: 0 10px 20px rgba(0,0,0,0.20);
}

/* headline ribbon */
.ribbon {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 999px;
  font-weight: 600;
  font-size: 12px;
  letter-spacing: .3px;
  background: rgba(34,197,94,0.18);
  border: 1px solid rgba(34,197,94,0.35);
  color: #86efac;
}

/* title */
.h1 {
  font-size: 28px;
  font-weight: 800;
  margin: 8px 0 0 0;
  letter-spacing: 0.3px;
}

/* subtitle */
.subtle {
  color: #9ca3af;
  font-size: 13px;
  margin-top: 6px;
}

/* green news output */
.news {
  background: white;
  border: 1px solid rgba(34,197,94,0.25);
  border-radius: 16px;
  padding: 14px 16px;
  color: black;
  line-height: 1.6;
  white-space: pre-wrap;
}

/* section headers */
.section-title {
  font-size: 14px;
  font-weight: 700;
  color: #cbd5e1;
  margin-bottom: 8px;
}

/* buttons */
.stButton>button {
  border-radius: 12px !important;
  padding: 10px 16px !important;
  font-weight: 700 !important;
  border: 1px solid rgba(255,255,255,0.12) !important;
  color : black !important;
}

/* success info */
.ok {
  color: #86efac;
}
</style>
""", unsafe_allow_html=True)

# ---------- Header Block ----------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<span class="ribbon">LATEST TECH NEWS THIS WEEK</span>', unsafe_allow_html=True)
st.markdown('<div class="h1">📰 Tech News Summarizer</div>', unsafe_allow_html=True)
st.markdown('<div class="subtle">Fetch the most important, most recent tech headlines, summarize beautifully, and optionally send to WhatsApp.</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------- Env / LLM / Tool Setup (logic unchanged) ----------
load_dotenv()


if "answer" not in st.session_state:
    st.session_state.answer = ""

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=api_key)

tavily_api_key = os.getenv("TAVILY_API_KEY")
search_engine = TavilySearch(
    max_results=5,
    tavily_api_key=tavily_api_key,
    topic="news"
)

# ---------- Topic selector ----------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Filters</div>', unsafe_allow_html=True)
topics = st.multiselect(
    "Select Topics",
    ["AI AND TECH", "Big Tech", "Startups", "Cybersecurity", "Product Launches", "Finance", "Crypto"],
    default=["AI AND TECH", "Big Tech", "Startups"]  # nice defaults
)
if topics:
    st.caption(f"Selected: {', '.join(topics)}")
st.markdown('</div>', unsafe_allow_html=True)

# ---------- Async fetch (logic unchanged) ----------
async def get_latest_news():
    result = search_engine.invoke({
        "query": f"Latest {topics} news from the past 7 days (AI, big tech, startups, cybersecurity, product launches). "
                 f"Return date in YYYY-MM-DD format. From Big News Websites;"
    })
    return result

# ---------- Action buttons row ----------
col1, col2 = st.columns([1, 1])
with col1:
    button = st.button("🔎 Get Latest News This Week")
with col2:
    # WhatsApp button is rendered below after news exists
    pass

# ---------- Agent-like Status + LLM formatting ----------
if button:
    st.session_state.whatsapp_sent = False
    with st.status("⏳ Searching…", expanded=True) as status:
        st.write("• Searching news sources with Tavily…")
        news = asyncio.run(get_latest_news())
        status.update(label="📥 Fetching relevant news this week…", state="running")
        st.write("• Parsing and collecting the most recent items…")
        status.update(label="🧠 Giving results to LLM for summarization…", state="running")

        # LLM formatting (logic preserved; only wrapped for UI)
        st.session_state.answer = llm.invoke(f"""
You are a professional news analyst.
Using the following search results:

{news}

Write a well-structured news digest with:
- Each news item as a bullet point
- Headline in **bold**
- Source and date in *italics* (YYYY-MM-DD)
- A 2–3 sentence detailed summary of the news, why it matters, and its impact
- Arrange news by recency and importance

Example format:
• **Meta Unveils Next-Gen VR Headset with Enhanced Eye-Tracking and Haptic Feedback** - *The Verge, 2023-10-26*  
  Meta launched its highly anticipated Quest 3 Pro VR headset, boasting significantly improved eye-tracking technology for more natural interactions and advanced haptic feedback in the controllers for a more immersive experience. This could mark a significant step forward in VR adoption, particularly in gaming and professional training simulations, as the improved technology addresses previous limitations.
""")
        status.update(label="✅ Done", state="complete")

# ---------- News Output (green style you requested) ----------
if st.session_state.answer:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">News Digest</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="news">{st.session_state.answer.content}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- WhatsApp send (logic unchanged; added spinner) ----------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Share</div>', unsafe_allow_html=True)



if not st.session_state.whatsapp_sent:
    send_whatsapp = st.button("📤 Send News Digest via WhatsApp")
    if send_whatsapp:
        if not st.session_state.answer:
            st.warning("Generate the news digest first before sending.")
        else:
            with st.spinner("Preparing WhatsApp message…"):
                time.sleep(3)  # 3–4s loading animation before the actual send
            kit.sendwhatmsg_instantly(
                "ENTER YOUR WHATSAPP NUMBER",
                st.session_state.answer.content,
                wait_time=10,
                tab_close=True,
                close_time=3
            )
            st.session_state.whatsapp_sent = True
            st.success("✅ Message sent via WhatsApp!")
else:
    st.info("Message already sent. Refresh to send again.")
st.markdown('</div>', unsafe_allow_html=True)
