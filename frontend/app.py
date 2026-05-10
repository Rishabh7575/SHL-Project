import streamlit as st
import requests
import os

st.set_page_config(page_title="SHL AI Assistant", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .block-container { padding-top: 2rem !important; padding-bottom: 2rem !important; }
    .recommendation-card {
        border: 1px solid rgba(128, 128, 128, 0.3);
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 16px;
        background-color: rgba(128, 128, 128, 0.05);
    }
    .recommendation-card h4 { margin-top: 0; margin-bottom: 8px; }
    .recommendation-card a { text-decoration: none; color: #1f77b4; }
    .recommendation-card p { margin-bottom: 0; font-style: italic; opacity: 0.85; font-size: 0.95em; }
    </style>
""", unsafe_allow_html=True)

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

def render_recommendation_card(rec):
    st.markdown(f"""
        <div class="recommendation-card">
            <h4><a href="{rec['url']}" target="_blank">{rec['assessment_name']}</a></h4>
            <p>{rec['reason']}</p>
        </div>
    """, unsafe_allow_html=True)

st.title("🤖 SHL Recommendation Assistant")
st.markdown("I can help you find the right SHL assessments for your candidates. Ask me anything!")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("recommendations"):
            st.markdown("### Top Recommendations:")
            for rec in msg["recommendations"]:
                render_recommendation_card(rec)

if prompt := st.chat_input("E.g., Suggest assessments for a Python Developer"):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                payload = {"messages": [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]}
                res = requests.post(API_URL, json=payload)
                res.raise_for_status()
                data = res.json().get("data", {})
                
                reply = data.get("reply", "No reply received.")
                recs = data.get("recommendations", [])
                
                st.markdown(reply)
                
                if recs:
                    st.markdown("### Top Recommendations:")
                    for r in recs:
                        render_recommendation_card(r)
                
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": reply,
                    "recommendations": recs
                })
                
            except requests.exceptions.RequestException as e:
                st.error(f"Error: {e}")
                st.session_state.messages.append({"role": "assistant", "content": f"Error: {e}"})

# fckkk solve the logo 