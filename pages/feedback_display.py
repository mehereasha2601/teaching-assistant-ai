import streamlit as st
import json
import re

# Custom CSS for better styling
st.markdown("""
    <style>
    /* Base styles */
    .stApp {
        background-color: #1a1a1a;
    }
    .main {
        background-color: #1a1a1a;
    }
    
    /* Text colors */
    .stMarkdown {
        color: #e0e0e0;
    }
    .stMarkdown p {
        color: #e0e0e0;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
        color: #4fc3f7;
    }
    .stMarkdown ul {
        color: #e0e0e0;
    }
    .stMarkdown li {
        color: #e0e0e0;
    }
    
    /* Cards and containers */
    .dashboard-card {
        background-color: #2d2d2d;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Section headers */
    .section-header {
        color: #4fc3f7;
        font-size: 1.2rem;
        margin: 1rem 0 0.5rem 0;
        font-weight: bold;
    }
    
    /* Feedback items */
    .feedback-item {
        background-color: #2d2d2d;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        color: #e0e0e0;
        border: 1px solid #404040;
    }
    
    /* Metric cards */
    .metric-card {
        background-color: #2d2d2d;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #4fc3f7;
    }
    .metric-label {
        color: #e0e0e0;
        font-size: 0.9rem;
    }
    
    /* Feedback categories */
    .strength {
        background-color: #1b5e20;
        padding: 0.5rem;
        border-radius: 4px;
        margin: 0.5rem 0;
        color: #e0e0e0;
    }
    .improvement {
        background-color: #0d47a1;
        padding: 0.5rem;
        border-radius: 4px;
        margin: 0.5rem 0;
        color: #e0e0e0;
    }
    .avoid {
        background-color: #b71c1c;
        padding: 0.5rem;
        border-radius: 4px;
        margin: 0.5rem 0;
        color: #e0e0e0;
    }
    </style>
    """, unsafe_allow_html=True)

def parse_feedback(feedback_text):
    """Parse the feedback text into structured data."""
    sections = {
        "overall": {
            "strengths": [],
            "improvements": [],
            "avoid": []
        },
        "planning": {},
        "environment": {},
        "instruction": {}
    }
    
    current_section = None
    current_subsection = None
    
    # Split the feedback into lines
    lines = feedback_text.split('\n')
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
            
        # Check for main sections
        if "Overall Feedback:" in line:
            current_section = "overall"
            continue
        elif "DOMAIN 1: PLANNING AND PREPARATION" in line:
            current_section = "planning"
            continue
        elif "DOMAIN 2: CLASSROOM ENVIRONMENT" in line:
            current_section = "environment"
            continue
        elif "DOMAIN 3: INSTRUCTION" in line:
            current_section = "instruction"
            continue
            
        # Check for overall feedback subsections
        if current_section == "overall":
            if "Strengths:" in line:
                current_subsection = "strengths"
                continue
            elif "Areas for Improvement:" in line:
                current_subsection = "improvements"
                continue
            elif "Avoid/Rethink:" in line:
                current_subsection = "avoid"
                continue
                
        # Check for domain subsections
        if current_section in ["planning", "environment", "instruction"]:
            if line.endswith(":"):
                current_subsection = line[:-1].strip()
                if current_subsection not in sections[current_section]:
                    sections[current_section][current_subsection] = []
                continue
                
        # Add content to current section
        if line.startswith("-"):
            content = line[1:].strip()
            if current_section == "overall" and current_subsection:
                sections["overall"][current_subsection].append(content)
            elif current_section in ["planning", "environment", "instruction"] and current_subsection:
                if current_subsection not in sections[current_section]:
                    sections[current_section][current_subsection] = []
                sections[current_section][current_subsection].append(content)
    
    return sections

def display_feedback_dashboard(feedback_text):
    """Display the feedback in a dashboard format."""
    sections = parse_feedback(feedback_text)
    
    # Display metrics
    st.markdown("### 📊 Feedback Overview")
    col1, col2, col3 = st.columns(3)
    
    total_points = sum(len(items) for domain in ["planning", "environment", "instruction"] 
                      for items in sections[domain].values())
    
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{total_points}</div>
                <div class="metric-label">Total Feedback Points</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">3</div>
                <div class="metric-label">Domains Covered</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{total_points//3 if total_points > 0 else 0}</div>
                <div class="metric-label">Points per Domain</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Display Overall Feedback
    st.markdown("### 📝 Overall Feedback")
    
    # Strengths
    if sections["overall"]["strengths"]:
        st.markdown("#### Strengths")
        for strength in sections["overall"]["strengths"]:
            st.markdown(f"- {strength}")
    
    # Areas for Improvement
    if sections["overall"]["improvements"]:
        st.markdown("#### Areas for Improvement")
        for improvement in sections["overall"]["improvements"]:
            st.markdown(f"- {improvement}")
    
    # Avoid/Rethink
    if sections["overall"]["avoid"]:
        st.markdown("#### Avoid/Rethink")
        for avoid in sections["overall"]["avoid"]:
            st.markdown(f"- {avoid}")
    
    # Display Domain 1: Planning and Preparation
    if sections["planning"]:
        st.markdown("### 📚 DOMAIN 1: PLANNING AND PREPARATION")
        for subcategory, items in sections["planning"].items():
            if items:  # Only display if there are items
                st.markdown(f"#### {subcategory}")
                for item in items:
                    st.markdown(f"- {item}")
    
    # Display Domain 2: Classroom Environment
    if sections["environment"]:
        st.markdown("### 🏫 DOMAIN 2: CLASSROOM ENVIRONMENT")
        for subcategory, items in sections["environment"].items():
            if items:  # Only display if there are items
                st.markdown(f"#### {subcategory}")
                for item in items:
                    st.markdown(f"- {item}")
    
    # Display Domain 3: Instruction
    if sections["instruction"]:
        st.markdown("### 👨‍🏫 DOMAIN 3: INSTRUCTION")
        for subcategory, items in sections["instruction"].items():
            if items:  # Only display if there are items
                st.markdown(f"#### {subcategory}")
                for item in items:
                    st.markdown(f"- {item}")

def main():
    st.markdown("""
        <div style='text-align: center;'>
            <h1>📊 Teaching Feedback Dashboard</h1>
            <p style='color: #666; font-size: 1rem;'>Detailed analysis of your teaching performance</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Check if feedback exists in session state
    if 'feedback' in st.session_state and st.session_state.feedback:
        display_feedback_dashboard(st.session_state.feedback)
        
        # Add download button for feedback
        feedback_text = st.session_state.feedback
        st.download_button(
            label="📥 Download Feedback Report",
            data=feedback_text,
            file_name="teaching_feedback_report.txt",
            mime="text/plain"
        )
    else:
        st.warning("No feedback available. Please generate feedback first.")

if __name__ == "__main__":
    main() 