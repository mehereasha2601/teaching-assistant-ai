from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
from openai_integration import OpenAIIntegration
from dotenv import load_dotenv
import os
import asyncio
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Teaching Assistant API",
    description="API for generating lecture plans and teaching feedback",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI integration with error handling
try:
    ai = OpenAIIntegration()
except Exception as e:
    print(f"Error initializing OpenAI integration: {str(e)}")
    raise

# Store for ongoing requests
ongoing_requests = {}

class FormData(BaseModel):
    grade: str
    topic: str
    country: str
    location: str
    number_of_students: str
    teaching_tenure_years: str
    percentage_of_girls: str
    percentage_of_boys: str
    attendance_percentage: str
    grade_level_competence: str
    classroom_challenges: str
    lecture_transcript: Optional[str] = None

def generate_lecture_plan_prompt(form_data: FormData) -> str:
    """Generate the prompt for lecture plan generation."""
    # Extract subject from topic
    subject = form_data.topic.split(' - ')[0] if ' - ' in form_data.topic else form_data.topic
    
    return f"""
    Create a detailed lecture plan for teaching {form_data.topic} to grade {form_data.grade} students.
    Consider the following context:
    - Class size: {form_data.number_of_students} students
    - Grade level competence: {form_data.grade_level_competence}
    - Location: {form_data.location}
    - Classroom challenges: {form_data.classroom_challenges}
    
    Please provide a structured lecture plan that includes:
    
    1. SUBTOPICS BREAKDOWN
    - List 4-6 key subtopics that should be covered
    - For each subtopic, provide:
      * A brief summary of the content
      * Estimated time allocation (in minutes)
      * Key learning objectives
    
    2. ENGAGEMENT STRATEGIES
    - For each subtopic, suggest:
      * An interactive activity or demonstration
      * A real-world example or application
      * A way to check for understanding
    
    3. DIFFERENTIATION STRATEGIES
    - How to support struggling students
    - How to challenge advanced students
    - How to maintain engagement for all ability levels
    
    4. TIMING AND PACING
    - Total lecture duration
    - Time allocation for each subtopic
    - Suggested breaks or transitions
    
    Format the response in a clear, structured way that's easy to follow.
    Consider the cultural context of {form_data.location} and the specific challenges mentioned.
    """

def generate_feedback_prompt(form_data: FormData) -> str:
    """Generate the prompt for feedback generation."""
    if not form_data.lecture_transcript:
        raise HTTPException(status_code=400, detail="Lecture transcript is required for feedback generation")
        
    # Extract subject from topic
    subject = form_data.topic.split(' - ')[0] if ' - ' in form_data.topic else form_data.topic
    
    return f"""
    We are teaching grade {form_data.grade} the topic {form_data.topic} in {form_data.country}. 
    My class is based out of {form_data.location}. There are {form_data.number_of_students} in my class, 
    {form_data.percentage_of_girls} of girls and {form_data.percentage_of_boys} of boys.
    The attendance is expected to be {form_data.attendance_percentage}, and the grade level competence 
    of my students is {form_data.grade_level_competence}. I have been teaching this grade for 
    {form_data.teaching_tenure_years}. The challenges I face are usually {form_data.classroom_challenges}. 
    
    Below is the transcript of my recent lecture. Please provide specific, actionable feedback based on the actual content of this lecture.
    For each point below, provide:
    1. A specific observation from the lecture
    2. A concrete suggestion for improvement
    3. An example of how to implement the suggestion

    LECTURE TRANSCRIPT:
    {form_data.lecture_transcript}
    
    Please provide feedback for EACH of the following points, specifically tailored for teaching {subject} at the {form_data.grade} grade level:

    DOMAIN 1: PLANNING AND PREPARATION
    1. Lecture Sequence: How well does the lecture sequence build understanding of {subject} concepts?
    2. Mixed Ability Levels: Are the examples and explanations appropriate for the mixed ability levels in {form_data.grade} grade?
    3. Key Concepts: How effectively are key {subject} concepts introduced and connected?
    4. Misconceptions: What specific misconceptions might {form_data.grade} grade students have about {subject}?
    5. Lesson Structure: How could the lesson be better structured for different learning levels in {form_data.grade} grade?

    DOMAIN 2: CLASSROOM ENVIRONMENT
    1. Student Engagement: How can the lecture be made more engaging for {form_data.grade} grade students with varying abilities?
    2. Attention Maintenance: What specific strategies could be used to maintain student attention during {subject} concepts?
    3. Content Relevance: How can the {subject} content be made more relevant to {form_data.grade} grade students' lives?
    4. Interactive Learning: What specific activities could be added to make the {subject} learning more interactive?
    5. Learning Styles: How can the lecture better accommodate different learning styles for {form_data.grade} grade students?

    DOMAIN 3: INSTRUCTION
    1. Problem-Solving Steps: How effectively are the steps for {subject} concepts explained?
    2. Visual Aids: What specific visual aids or examples could enhance understanding of {subject}?
    3. Concept Explanation: How could the explanation of key {subject} concepts be improved?
    4. Practice Opportunities: What specific practice opportunities could be added for {form_data.grade} grade level?
    5. Differentiated Instruction: How could the lecture better address the needs of students at different grade levels?

    For each point above, provide specific examples and concrete suggestions that can be implemented immediately in the classroom.
    Consider the cultural context of {form_data.location} and the specific challenges mentioned: {form_data.classroom_challenges}.
    """

async def generate_response(request_id: str, prompt: str):
    """Generate response asynchronously"""
    try:
        response = ai.get_response(prompt)
        if response:
            ongoing_requests[request_id] = {
                "status": "completed",
                "data": response
            }
        else:
            ongoing_requests[request_id] = {
                "status": "error",
                "error": "Failed to generate response"
            }
    except Exception as e:
        ongoing_requests[request_id] = {
            "status": "error",
            "error": str(e)
        }

@app.post("/generate-lecture-plan")
async def generate_lecture_plan(form_data: FormData, background_tasks: BackgroundTasks):
    """Generate a lecture plan based on form data."""
    try:
        # Generate unique request ID
        request_id = f"lecture_plan_{len(ongoing_requests)}"
        
        # Initialize request status
        ongoing_requests[request_id] = {"status": "processing"}
        
        # Generate prompt
        prompt = generate_lecture_plan_prompt(form_data)
        
        # Start background task
        background_tasks.add_task(generate_response, request_id, prompt)
        
        return {
            "status": "processing",
            "request_id": request_id,
            "message": "Request accepted. Use the request_id to check status."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-feedback")
async def generate_feedback(form_data: FormData, background_tasks: BackgroundTasks):
    """Generate teaching feedback based on form data and lecture transcript."""
    try:
        if not form_data.lecture_transcript:
            raise HTTPException(status_code=400, detail="Lecture transcript is required")
        
        # Generate unique request ID
        request_id = f"feedback_{len(ongoing_requests)}"
        
        # Initialize request status
        ongoing_requests[request_id] = {"status": "processing"}
        
        # Generate prompt
        prompt = generate_feedback_prompt(form_data)
        
        # Start background task
        background_tasks.add_task(generate_response, request_id, prompt)
        
        return {
            "status": "processing",
            "request_id": request_id,
            "message": "Request accepted. Use the request_id to check status."
        }
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status/{request_id}")
async def get_status(request_id: str):
    """Get the status of a request"""
    if request_id not in ongoing_requests:
        raise HTTPException(status_code=404, detail="Request not found")
    
    status = ongoing_requests[request_id]
    
    if status["status"] == "completed":
        # Clean up completed request
        response_data = ongoing_requests.pop(request_id)
        return {
            "status": "success",
            "data": response_data["data"]
        }
    elif status["status"] == "error":
        # Clean up failed request
        error_data = ongoing_requests.pop(request_id)
        raise HTTPException(status_code=500, detail=error_data["error"])
    else:
        return {
            "status": "processing",
            "message": "Request is still being processed"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 