# app.py -- LinkedIn Bio Roaster
# Powered by Groq + LLaMA 3  |  Built at DataYard

import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(
    page_title="LinkedIn Bio Roaster",
    page_icon="🔥",
    layout="centered"
)

st.title("🔥 LinkedIn Bio Roaster")
st.caption("Powered by LLaMA 3 via Groq")
st.divider()

# Connect to Groq using the API key stored in Streamlit secrets
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Intensity slider
intensity = st.select_slider(
    "Roast Intensity",
    options=["Mild", "Medium", "Savage", "Brutal"],
    value="Savage"
)

# System prompt for each intensity level
PROMPTS = {
    "Mild": """You are a kind but honest LinkedIn bio reviewer.
Point out cliches and buzzwords with light humour.
Be encouraging. End with 2 specific genuine compliments.""",

    "Medium": """You are a witty LinkedIn bio roaster.
Call out buzzwords, humble-brags, and corporate speak with sharp humour.
Be funny but not cruel. End with one genuine compliment.""",

    "Savage": """You are a savage LinkedIn bio roaster with zero tolerance for nonsense.
Destroy the buzzwords, dismantle the humble-brags, mock the cliches mercilessly.
Be hilarious and cutting. End with one tiny genuine compliment.""",

    "Brutal": """You are the most ruthless LinkedIn bio critic alive.
Eviscerate this bio. Name every buzzword. Destroy every humble-brag.
Be absolutely savage. End with one sentence of genuine feedback."""
}

# Bio input
bio = st.text_area(
    "Paste your LinkedIn bio here",
    height=200,
    placeholder="Passionate results-driven thought leader who leverages synergies..."
)

# Roast button and API call
if st.button("Roast Me", type="primary", use_container_width=True):
    if not bio.strip():
        st.warning("Paste a bio first.")
    else:
        with st.spinner("Roasting..."):
            response = client.chat.completions.create(
                model="llama3-8b-8192",
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
