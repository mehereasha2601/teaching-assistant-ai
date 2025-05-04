import streamlit as st
from openai_integration import OpenAIIntegration
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI integration
ai = OpenAIIntegration()

# Initialize session state for lecture plan
if 'lecture_plan' not in st.session_state:
    st.session_state.lecture_plan = None

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
    .lecture-plan-box {
        background-color: #e8f5e9;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .subtopic-box {
        background-color: #f1f8e9;
        padding: 0.5rem;
        border-radius: 8px;
        margin: 0.25rem 0;
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
    </style>
    """, unsafe_allow_html=True)

def generate_lecture_plan(form_data):
    """Generate a lecture plan based on form data."""
    
    # Extract subject from topic
    subject = form_data['topic'].split(' - ')[0] if ' - ' in form_data['topic'] else form_data['topic']
    
    # Create dynamic prompt based on subject and grade level
    prompt = f"""
    Create a detailed lecture plan for teaching {subject} to {form_data['grade']} grade students. The class is based at {form_data['location']} in {form_data['country']} with {form_data['number_of_students']} students ({form_data['percentage_of_girls']} girls, {form_data['percentage_of_boys']} boys). The teacher has {form_data['teaching_tenure_years']} of experience, and the class has {form_data['attendance_percentage']} attendance with {form_data['grade_level_competence']} competence level. Current challenges include: {form_data['classroom_challenges']}.

    Please structure your response EXACTLY as follows:

    Overview:
    - [Write 2-3 bullet points about the topic's importance and relevance]
    - [Include how it connects to previous and future learning]
    - [Add any key context for this specific class]

    Learning Objectives:
    - [List 3-5 specific, measurable objectives]
    - [Each objective should be achievable within the class period]
    - [Include objectives for different learning levels]

    Materials:
    - [List all required physical materials]
    - [Include any digital resources needed]
    - [Note any preparation required]

    Timeline:
    - [Break down the class into 5-10 minute segments]
    - [Include specific activities for each segment]
    - [Note when to check for understanding]
    - [Include time for questions and discussion]

    Assessment:
    - [List specific ways to check understanding]
    - [Include quick assessment methods]
    - [Add questions to ask students]
    - [Note activities to verify learning]

    Important: 
    1. Start each section with the exact header shown above
    2. Use bullet points (starting with -) for all items
    3. Keep each bullet point concise and clear
    4. Maintain this exact structure for proper parsing
    """
    
    return ai.get_response(prompt)

def main():
    st.markdown("""
        <div style='text-align: center;'>
            <h1>✨ Lecture Plan Generator</h1>
            <p style='color: #666; font-size: 1rem;'>Create comprehensive lecture plans for your class</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📋 Class Information")
    
    with st.form("lecture_plan_form"):
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        
        # Row 1
        st.markdown('<div class="form-row">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            form_data = {
                'grade': st.text_input("Grade Level", "8th", help="Enter the grade level you're teaching"),
                'topic': st.text_input("Topic", "Algebra - Linear Equations", help="Enter the specific topic being taught"),
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
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Generate plan button
        submitted = st.form_submit_button("✨ Generate Lecture Plan", type="primary")
        
        if submitted:
            with st.spinner("🤔 Generating your lecture plan..."):
                plan = generate_lecture_plan(form_data)
                
                if plan:
                    st.session_state.lecture_plan = plan
                    st.success("✅ Lecture plan generated successfully!")
                    # Redirect to lecture plan display page
                    st.switch_page("pages/lecture_plan_display.py")
                else:
                    st.error("❌ Failed to generate lecture plan. Please check your API key and try again.")

if __name__ == "__main__":
    main() 