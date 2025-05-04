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
    
    /* Plan items */
    .plan-item {
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
    
    /* Timeline */
    .timeline-item {
        background-color: #2d2d2d;
        padding: 0.5rem;
        border-radius: 4px;
        margin: 0.5rem 0;
        color: #e0e0e0;
        border-left: 3px solid #4fc3f7;
    }
    
    /* Objectives */
    .objective {
        background-color: #1b5e20;
        padding: 0.5rem;
        border-radius: 4px;
        margin: 0.5rem 0;
        color: #e0e0e0;
    }
    
    /* Materials */
    .material {
        background-color: #0d47a1;
        padding: 0.5rem;
        border-radius: 4px;
        margin: 0.5rem 0;
        color: #e0e0e0;
    }
    
    /* Assessment */
    .assessment {
        background-color: #b71c1c;
        padding: 0.5rem;
        border-radius: 4px;
        margin: 0.5rem 0;
        color: #e0e0e0;
    }
    </style>
    """, unsafe_allow_html=True)

def parse_lecture_plan(plan_text):
    """Parse the lecture plan text into structured data."""
    sections = {
        "Overview": [],
        "Learning Objectives": [],
        "Materials": [],
        "Timeline": [],
        "Assessment": []
    }
    
    current_section = None
    
    # Split the plan into lines
    lines = plan_text.split('\n')
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
            
        # Check for section headers
        if line.startswith("Overview:"):
            current_section = "Overview"
            continue
        elif line.startswith("Learning Objectives:"):
            current_section = "Learning Objectives"
            continue
        elif line.startswith("Materials:"):
            current_section = "Materials"
            continue
        elif line.startswith("Timeline:"):
            current_section = "Timeline"
            continue
        elif line.startswith("Assessment:"):
            current_section = "Assessment"
            continue
            
        # Add content to current section
        if current_section:
            if line.startswith("- "):
                sections[current_section].append(line[2:])
            else:
                sections[current_section].append(line)
    
    return sections

def display_lecture_plan_dashboard(plan_text):
    """Display the lecture plan in a dashboard format."""
    sections = parse_lecture_plan(plan_text)
    
    # Display header
    st.markdown("""
        <div style='text-align: center;'>
            <h1 style='color: #1f77b4; font-size: 2rem; margin-bottom: 1rem;'>Lecture Plan Analysis</h1>
            <p style='color: #666; font-size: 1.1rem;'>Comprehensive breakdown of your lecture plan</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Display metrics
    st.markdown('<div class="section-title">📊 Plan Overview</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(sections['Learning Objectives'])}</div>
                <div class="metric-label">Learning Objectives</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(sections['Timeline'])}</div>
                <div class="metric-label">Timeline Items</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(sections['Assessment'])}</div>
                <div class="metric-label">Assessment Points</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Display Overview
    st.markdown('<div class="section-title">📝 Overview</div>', unsafe_allow_html=True)
    for item in sections['Overview']:
        st.markdown(f"""
            <div class="plan-item">
                <div class="overview">
                    <span class="plan-text">{item}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Display Learning Objectives
    st.markdown('<div class="section-title">🎯 Learning Objectives</div>', unsafe_allow_html=True)
    for objective in sections['Learning Objectives']:
        st.markdown(f"""
            <div class="plan-item">
                <div class="objective">
                    <span class="plan-text">{objective}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Display Materials
    st.markdown('<div class="section-title">📚 Materials</div>', unsafe_allow_html=True)
    for material in sections['Materials']:
        st.markdown(f"""
            <div class="plan-item">
                <div class="material">
                    <span class="plan-text">{material}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Display Timeline
    st.markdown('<div class="section-title">⏱️ Timeline</div>', unsafe_allow_html=True)
    st.markdown('<div class="timeline">', unsafe_allow_html=True)
    for item in sections['Timeline']:
        st.markdown(f"""
            <div class="timeline-item">
                <span class="plan-text">{item}</span>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display Assessment
    st.markdown('<div class="section-title">📊 Assessment</div>', unsafe_allow_html=True)
    for assessment in sections['Assessment']:
        st.markdown(f"""
            <div class="plan-item">
                <div class="assessment">
                    <span class="plan-text">{assessment}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

def main():
    # Check if lecture plan exists in session state
    if 'lecture_plan' not in st.session_state:
        st.warning("No lecture plan available. Please generate a plan first.")
        return
    
    # Display the dashboard
    display_lecture_plan_dashboard(st.session_state.lecture_plan)
    
    # Add download button
    st.download_button(
        label="📥 Download Lecture Plan",
        data=st.session_state.lecture_plan,
        file_name="lecture_plan.md",
        mime="text/markdown",
        help="Download the lecture plan as a markdown file"
    )

if __name__ == "__main__":
    main() 