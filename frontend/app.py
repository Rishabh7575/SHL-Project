import streamlit as st
import requests
import os

# Configure the page
st.set_page_config(
    page_title="SHL AI Assistant",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS for spacing and card layout
st.markdown("""
    <style>
    /* Reduce top padding for a tighter layout */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }
    /* Card style for recommendations */
    .recommendation-card {
        border: 1px solid rgba(128, 128, 128, 0.3);
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 16px;
        background-color: rgba(128, 128, 128, 0.05);
    }
    .recommendation-card h4 {
        margin-top: 0;
        margin-bottom: 8px;
    }
    .recommendation-card a {
        text-decoration: none;
        color: #1f77b4; /* A nice accessible blue */
    }
    .recommendation-card p {
        margin-bottom: 0;
        font-style: italic;
        opacity: 0.85;
        font-size: 0.95em;
    }
    </style>
""", unsafe_allow_html=True)

# Use environment variable for deployed backend, fallback to local
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/chat")

# Initialize session state for conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Helper function to render a recommendation card
def render_recommendation_card(rec):
    st.markdown(f"""
        <div class="recommendation-card">
            <h4><a href="{rec['url']}" target="_blank">{rec['assessment_name']}</a></h4>
            <p>{rec['reason']}</p>
        </div>
    """, unsafe_allow_html=True)

# Title and header
st.title("🤖 SHL Recommendation Assistant")
st.markdown("I can help you find the right SHL assessments for your candidates. Ask me anything!")

# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Display recommendations if they exist in this message
        if "recommendations" in message and message["recommendations"]:
            st.markdown("### Top Recommendations:")
            for rec in message["recommendations"]:
                render_recommendation_card(rec)

# Input area for user queries
if prompt := st.chat_input("E.g., Suggest assessments for a Python Developer"):
    # 1. Display user message immediately
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 2. Add to session state history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 3. Call the FastAPI backend
    with st.chat_message("assistant"):
        with st.spinner("Searching and thinking..."):
            try:
                # Prepare payload according to ChatRequest schema
                payload = {
                    "messages": [
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ]
                }
                
                response = requests.post(API_URL, json=payload)
                response.raise_for_status()
                data = response.json()
                
                reply = data.get("data", {}).get("reply", "No reply received.")
                recommendations = data.get("data", {}).get("recommendations", [])
                
                # Display the conversational reply
                st.markdown(reply)
                
                # Display the recommendation cards
                if recommendations:
                    st.markdown("### Top Recommendations:")
                    for rec in recommendations:
                        render_recommendation_card(rec)
                
                # Add assistant response to session state
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": reply,
                    "recommendations": recommendations
                })
                
            except requests.exceptions.RequestException as e:
                error_msg = f"Error connecting to backend: {e}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
