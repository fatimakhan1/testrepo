# app.py -- LinkedIn Bio Roaster
# Powered by Groq + LLaMA 3  |  Built at DataYard
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="LinkedIn Bio Roaster",
    page_icon="🔥",
    layout="centered"
)
st.title("🔥 LinkedIn Bio Roaster")
st.caption("Powered by LLaMA 3 via Groq")
st.divider()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

intensity = st.select_slider(
    "Roast Intensity",
    options=["Mild", "Medium", "Savage", "Brutal"],
    value="Savage"
)

PROMPTS = {
    "Mild": """You are a kind but honest LinkedIn bio reviewer.
Point out cliches and buzzwords with light humour.
Be encouraging. End with 2 specific genuine compliments.
Use simple, conversational language. Keep it short and easy to read.""",

    "Medium": """You are a witty LinkedIn bio roaster.
Call out buzzwords and humble-brags with sharp humour.
Be funny but not cruel. End with one genuine compliment.
Write like a funny friend, not a professor. Keep sentences short.""",

    "Savage": """You are a savage LinkedIn bio roaster.
Destroy the buzzwords and cliches. Be hilarious and cutting.
End with one tiny genuine compliment.
Write in short punchy sentences. Simple words only. No complex vocabulary.""",

    "Brutal": """You are the most ruthless LinkedIn bio critic alive.
Tear this bio apart. Call out every buzzword and every humble-brag.
Be savage and funny. End with one honest sentence of feedback.
IMPORTANT: Write like you are texting a friend. Short sentences. Simple words.
No complex vocabulary. No fancy phrases. Just brutal, funny, plain English."""
}

bio = st.text_area(
    "Paste your LinkedIn bio here",
    height=200,
    placeholder="Passionate results-driven thought leader who leverages synergies..."
)

if st.button("Roast Me", type="primary", use_container_width=True):
    if not bio.strip():
        st.warning("Paste a bio first.")
    else:
        with st.spinner("Roasting..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": PROMPTS[intensity]},
                    {"role": "user",   "content": f"Roast this LinkedIn bio:\n\n{bio}"}
                ]
            )
            roast = response.choices[0].message.content
        st.divider()
        st.subheader(f"{intensity} Roast")
        st.write(roast)
        st.divider()

st.divider()
st.caption("Built at DataYard  |  Powered by Groq + LLaMA 3")
