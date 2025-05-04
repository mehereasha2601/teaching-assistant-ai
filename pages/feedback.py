import streamlit as st
from openai_integration import OpenAIIntegration
from dotenv import load_dotenv
import io
import json
import re

# Load environment variables
load_dotenv()

# Initialize OpenAI integration
ai = OpenAIIntegration()

# Initialize session state for feedback
if 'feedback' not in st.session_state:
    st.session_state.feedback = None

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0.5rem;
        background-color: white;
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
    .stTextInput>div>div>input {
        border-radius: 5px;
        padding: 0.25rem 0.5rem;
    }
    .stTextArea>div>div>textarea {
        border-radius: 5px;
        padding: 0.25rem 0.5rem;
    }
    .feedback-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .upload-box {
        background-color: #e8f5e9;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border: 2px dashed #4CAF50;
    }
    .upload-box:hover {
        background-color: #f1f8e9;
    }
    .dashboard-card {
        background-color: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .domain-header {
        color: #1f77b4;
        font-size: 1.5rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e0e0e0;
    }
    .feedback-item {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .feedback-item h4 {
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    .observation {
        background-color: #e3f2fd;
        padding: 0.5rem;
        border-radius: 4px;
        margin: 0.5rem 0;
    }
    .suggestion {
        background-color: #e8f5e9;
        padding: 0.5rem;
        border-radius: 4px;
        margin: 0.5rem 0;
    }
    .example {
        background-color: #fff3e0;
        padding: 0.5rem;
        border-radius: 4px;
        margin: 0.5rem 0;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        margin: 0.5rem;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .metric-label {
        color: #666;
        font-size: 0.9rem;
    }
    h1 {
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
        font-size: 1.75rem;
    }
    h2 {
        color: #2c3e50;
        margin-bottom: 0.5rem;
        font-size: 1.25rem;
    }
    .form-container {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        width: 100%;
    }
    .form-row {
        display: flex;
        gap: 0.5rem;
        width: 100%;
    }
    .form-field {
        flex: 1;
    }
    .form-section {
        margin-bottom: 1rem;
        width: 100%;
    }
    div[data-testid="stForm"] {
        width: 100%;
    }
    div[data-testid="stForm"] > div {
        width: 100%;
    }
    .domain-select {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

def parse_feedback(feedback_text):
    """Parse the feedback text into structured data."""
    domains = {
        "PLANNING AND PREPARATION": [],
        "CLASSROOM ENVIRONMENT": [],
        "INSTRUCTION": []
    }
    
    current_domain = None
    current_item = None
    
    # Split the feedback into lines
    lines = feedback_text.split('\n')
    
    for line in lines:
        line = line.strip()
        
        # Check for domain headers
        if "DOMAIN" in line:
            current_domain = line.split(":")[1].strip()
            continue
            
        # Check for numbered items
        if re.match(r'^\d+\.', line):
            if current_item:
                domains[current_domain].append(current_item)
            current_item = {
                "title": line.split('.', 1)[1].strip(),
                "observation": "",
                "suggestion": "",
                "example": ""
            }
            continue
            
        # Add content to current item
        if current_item:
            if "observation" in line.lower():
                current_item["observation"] = line.split(":", 1)[1].strip() if ":" in line else line
            elif "suggestion" in line.lower():
                current_item["suggestion"] = line.split(":", 1)[1].strip() if ":" in line else line
            elif "example" in line.lower():
                current_item["example"] = line.split(":", 1)[1].strip() if ":" in line else line
    
    # Add the last item
    if current_item and current_domain:
        domains[current_domain].append(current_item)
    
    return domains

def display_feedback_dashboard(feedback_text):
    """Display the feedback in a dashboard format."""
    domains = parse_feedback(feedback_text)
    
    # Display metrics
    st.markdown("### 📊 Feedback Overview")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">15</div>
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
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">5</div>
                <div class="metric-label">Points per Domain</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Display each domain
    for domain, items in domains.items():
        st.markdown(f"""
            <div class="dashboard-card">
                <div class="domain-header">📚 {domain}</div>
            </div>
        """, unsafe_allow_html=True)
        
        for item in items:
            st.markdown(f"""
                <div class="feedback-item">
                    <h4>{item['title']}</h4>
                    <div class="observation">
                        <strong>Observation:</strong> {item['observation']}
                    </div>
                    <div class="suggestion">
                        <strong>Suggestion:</strong> {item['suggestion']}
                    </div>
                    <div class="example">
                        <strong>Example:</strong> {item['example']}
                    </div>
                </div>
            """, unsafe_allow_html=True)

def generate_feedback(form_data):
    """Generate feedback based on form data."""
    
    # Create dynamic prompt based on selected domain
    prompt = f"""
    As an expert in teaching and pedagogy, analyze the following lecture transcript and provide detailed feedback 
    for a {form_data['grade']} grade class at {form_data['location']} in {form_data['country']}. The class has 
    {form_data['number_of_students']} students with {form_data['percentage_of_girls']} girls and {form_data['percentage_of_boys']} boys. 
    The attendance is {form_data['attendance_percentage']}, and the grade level competence is {form_data['grade_level_competence']}. 
    The teacher has been teaching this grade for {form_data['teaching_tenure_years']} and faces challenges such as 
    {form_data['classroom_challenges']}.

    Lecture Transcript:
    {form_data['lecture_transcript']}

    Please structure your response EXACTLY as follows:

    Overall Feedback:
    Strengths:
    - [List 2-3 key strengths observed]
    - [Include specific examples from transcript]

    Areas for Improvement:
    - [List 2-3 areas needing attention]
    - [Include specific examples from transcript]

    Avoid/Rethink:
    - [List 1-2 practices to reconsider]
    - [Include specific examples from transcript]

    DOMAIN 1: PLANNING AND PREPARATION
    Knowledge of Content and Pedagogy:
    - [Observation with evidence]
    - [Suggestion for improvement]
    - [Specific example from transcript]

    Lesson Design and Coherence:
    - [Observation with evidence]
    - [Suggestion for improvement]
    - [Specific example from transcript]

    Knowledge of Students and Differentiation:
    - [Observation with evidence]
    - [Suggestion for improvement]
    - [Specific example from transcript]

    Use of Resources and Materials:
    - [Observation with evidence]
    - [Suggestion for improvement]
    - [Specific example from transcript]

    Assessment Integration:
    - [Observation with evidence]
    - [Suggestion for improvement]
    - [Specific example from transcript]

    DOMAIN 2: CLASSROOM ENVIRONMENT
    Respectful Interactions and Relationships:
    - [Observation with evidence]
    - [Suggestion for improvement]
    - [Specific example from transcript]

    High Expectations and Intellectual Engagement:
    - [Observation with evidence]
    - [Suggestion for improvement]
    - [Specific example from transcript]

    Classroom Procedures and Time Management:
    - [Observation with evidence]
    - [Suggestion for improvement]
    - [Specific example from transcript]

    Student Behavior Management:
    - [Observation with evidence]
    - [Suggestion for improvement]
    - [Specific example from transcript]

    Physical Space Organization:
    - [Observation with evidence]
    - [Suggestion for improvement]
    - [Specific example from transcript]

    DOMAIN 3: INSTRUCTION
    Communication of Purpose and Directions:
    - [Observation with evidence]
    - [Suggestion for improvement]
    - [Specific example from transcript]

    Quality of Explanations and Scaffolding:
    - [Observation with evidence]
    - [Suggestion for improvement]
    - [Specific example from transcript]

    Discussion Techniques and Questioning:
    - [Observation with evidence]
    - [Suggestion for improvement]
    - [Specific example from transcript]

    Student Engagement and Participation:
    - [Observation with evidence]
    - [Suggestion for improvement]
    - [Specific example from transcript]

    Responsive Teaching and Assessment Use:
    - [Observation with evidence]
    - [Suggestion for improvement]
    - [Specific example from transcript]

    Important:
    1. Start each section with the exact header shown above
    2. Use bullet points (starting with -) for all items
    3. Keep each bullet point concise and clear
    4. Maintain this exact structure for proper parsing
    5. Provide specific evidence from the transcript for each observation
    6. Make suggestions actionable and immediately implementable
    7. Focus on concrete examples and specific moments from the transcript
    """
    
    return ai.get_response(prompt)

def read_uploaded_file(uploaded_file):
    """Read content from uploaded file."""
    if uploaded_file is not None:
        try:
            # Read the file content
            content = uploaded_file.getvalue().decode("utf-8")
            return content
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
            return None
    return None

def main():
    st.markdown("""
        <div style='text-align: center;'>
            <h1>✨ Teaching Feedback Generator</h1>
            <p style='color: #666; font-size: 1rem;'>Get detailed feedback on your teaching</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📋 Class Information")
    
    with st.form("feedback_form"):
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        
        # Row 1
        st.markdown('<div class="form-row">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            form_data = {
                'grade': st.text_input("Grade Level", "8th", help="Enter the grade level you're teaching"),
                'country': st.text_input("Country", "United States", help="Enter the country where you're teaching"),
                'location': st.text_input("School Location", "Santa Fe Indian School", help="Enter your school's location"),
                'number_of_students': st.text_input("Number of Students", "25", help="Total number of students in the class"),
            }
        with col2:
            form_data.update({
                'teaching_tenure_years': st.text_input("Teaching Tenure", "5 years", help="How long you've been teaching this grade"),
                'percentage_of_girls': st.text_input("Percentage of Girls", "48%", help="Percentage of female students"),
                'percentage_of_boys': st.text_input("Percentage of Boys", "52%", help="Percentage of male students"),
                'attendance_percentage': st.text_input("Expected Attendance", "92%", help="Expected attendance rate"),
                'grade_level_competence': st.text_input("Grade Level Competence", "mixed, ranging from 6th to 9th grade level", help="Describe the overall competence level of your students"),
            })
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Classroom Challenges Section
        form_data['classroom_challenges'] = st.text_area(
            "Classroom Challenges",
            "varying levels of mathematical preparedness, engagement during abstract concepts, and maintaining consistent attendance",
            help="Describe the main challenges you face in the classroom",
            height=100
        )
        
        # Domain Selection
        st.markdown('<div class="domain-select">', unsafe_allow_html=True)
        st.markdown("### 🎯 Select Domain for Feedback")
        domains = [
            "Classroom Management",
            "Student Engagement",
            "Content Delivery",
            "Assessment & Feedback",
            "Differentiation",
            "Technology Integration",
            "Cultural Responsiveness",
            "Questioning Techniques",
            "Time Management",
            "Student Support"
        ]
        form_data['domain'] = st.selectbox(
            "Choose the domain you want feedback on",
            domains,
            help="Select the specific aspect of teaching you want feedback on"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Lecture Transcript Section
        st.markdown("### 📝 Lecture Transcript")
        st.markdown("""
            <div class="upload-box">
                <p style='text-align: center; margin-bottom: 0.5rem;'>
                    Upload your lecture transcript or paste it below
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # File Upload
        uploaded_file = st.file_uploader(
            "Upload Transcript",
            type=['txt', 'md', 'doc', 'docx'],
            help="Upload your lecture transcript file"
        )
        
        # Text Area for Manual Input
        form_data['lecture_transcript'] = st.text_area(
            "Or paste your lecture transcript here",
            height=200,
            help="Paste your lecture transcript if you don't have a file"
        )
        
        # If file is uploaded, read its content
        if uploaded_file is not None:
            file_content = read_uploaded_file(uploaded_file)
            if file_content:
                form_data['lecture_transcript'] = file_content
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Generate feedback button
        submitted = st.form_submit_button("✨ Generate Feedback", type="primary")
        
        if submitted:
            if not form_data['lecture_transcript']:
                st.error("❌ Please provide a lecture transcript to generate feedback.")
            else:
                with st.spinner("🤔 Generating your feedback..."):
                    feedback = generate_feedback(form_data)
                    
                    if feedback:
                        st.session_state.feedback = feedback
                        st.success("✅ Feedback generated successfully!")
                        # Redirect to feedback display page
                        st.switch_page("pages/feedback_display.py")
                    else:
                        st.error("❌ Failed to generate feedback. Please check your API key and try again.")

if __name__ == "__main__":
    main() 