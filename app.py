import streamlit as st
from groq import Groq
 
# Page configuration
st.set_page_config(
    page_title="WorkMate",
    page_icon="💼",
    layout="centered"
)
 
# Header
st.title("💼 WorkMate")
st.caption("Your AI assistant for working professionals")
st.divider()
 
# Mode definitions — each mode has its own system prompt
MODES = {
    "📧 Email Coach": (
        "You are an expert email coach for working professionals. "
        "Help users draft, polish, and improve work emails. "
        "Keep suggestions clear, professional, and concise. "
        "Always provide ready-to-use text the user can copy and send."
    ),
    "💬 Slack Coach": (
        "You are a Slack communication coach for working professionals. "
        "Help users write clear, friendly, and effective workplace messages. "
        "Watch the tone — no passive-aggressive vibes, no stiff corporate-speak. "
        "Provide ready-to-send messages."
    ),
    "📋 Meeting Prep": (
        "You are a meeting preparation coach. Help the user prepare "
        "for upcoming meetings by suggesting talking points, anticipating "
        "questions, structuring agendas, and identifying clear outcomes. "
        "Keep advice specific and actionable."
    ),
    "🧠 Brainstorm": (
        "You are a thinking partner for working professionals. Help the user "
        "think through work problems, generate ideas, weigh trade-offs, and "
        "explore options. Ask clarifying questions when useful. Be direct, "
        "structured, and curious."
    ),
}
 
# Sidebar — mode selector and conversation reset
with st.sidebar:
    st.header("Settings")
    mode = st.selectbox(
        "Mode",
        options=list(MODES.keys()),
        index=0,
    )
    st.caption("Switch modes anytime to change how WorkMate helps you.")
 
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
 
# Initialise chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []
 
# Display previous chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
 
# Chat input — runs every time the user submits
if prompt := st.chat_input("Ask anything..."):
    # Save and display the user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
 
    # Build the API request: system prompt + entire chat history
    api_messages = [{"role": "system", "content": MODES[mode]}]
    api_messages.extend(st.session_state.messages)
 
    # Call Groq and stream the reply into a chat bubble
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=api_messages,
                    temperature=0.7,
                )
                reply = completion.choices[0].message.content
            except Exception as e:
                reply = f"Error: {str(e)}"
        st.write(reply)
 
    # Save the assistant reply to history
    st.session_state.messages.append({"role": "assistant", "content": reply})
