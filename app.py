import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="Teaching Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0.5rem;
        background-color: white;
        max-width: 1200px;
        margin: 0 auto;
    }
    .stButton>button {
        width: 100%;
        margin-top: 0.5rem;
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .feature-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.25rem 0;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        height: 300px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .feature-card h2 {
        color: #1f77b4;
        margin-bottom: 0.25rem;
        font-size: 1.5rem;
    }
    .feature-card p {
        color: #333;
        margin-bottom: 0.25rem;
        font-size: 1rem;
    }
    .feature-card ul {
        color: #333;
        text-align: left;
        margin: 0.25rem 0;
        padding-left: 1.5rem;
        font-size: 0.9rem;
        list-style-type: none;
    }
    .feature-card li {
        margin: 0.15rem 0;
        position: relative;
        padding-left: 1.5rem;
    }
    .feature-card li:before {
        content: "•";
        position: absolute;
        left: 0;
        color: #4CAF50;
    }
    h1 {
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.25rem;
        font-size: 2rem;
    }
    .subtitle {
        color: #666;
        font-size: 1.1rem;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .stMarkdown {
        margin-bottom: 0;
    }
    .column {
        display: flex;
        flex-direction: column;
        height: 100%;
    }
    .button-container {
        margin-top: auto;
        padding-top: 0.5rem;
    }
    .header-container {
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .content-container {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
    }
    .card-content {
        flex: 1;
        display: flex;
        flex-direction: column;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    # Header with icon
    st.markdown("""
        <div class='header-container'>
            <h1>📚 Teaching Assistant</h1>
            <p class='subtitle'>Your AI-powered teaching companion</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Content container
    st.markdown('<div class="content-container">', unsafe_allow_html=True)
    
    # Create two columns for feature cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class='feature-card'>
                <div class='card-content'>
                    <h2>📝 Lecture Plan Generator</h2>
                    <p>Generate detailed, personalized lecture plans with:</p>
                    <ul>
                        <li>Subtopics breakdown</li>
                        <li>Time allocations</li>
                        <li>Engagement strategies</li>
                        <li>Differentiation techniques</li>
                    </ul>
                </div>
                <div class='button-container'>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Create Lecture Plan", key="lecture_plan"):
            st.switch_page("pages/lecture_plan.py")
    
    with col2:
        st.markdown("""
            <div class='feature-card'>
                <div class='card-content'>
                    <h2>✨ Teaching Feedback</h2>
                    <p>Get comprehensive feedback on your teaching with:</p>
                    <ul>
                        <li>Planning and preparation analysis</li>
                        <li>Classroom environment insights</li>
                        <li>Instruction effectiveness</li>
                        <li>Actionable improvements</li>
                    </ul>
                </div>
                <div class='button-container'>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Get Teaching Feedback", key="feedback"):
            st.switch_page("pages/feedback.py")
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main() 