import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

# Test data
test_form_data = {
    "grade": "8th",
    "topic": "Algebra - Linear Equations",
    "country": "United States",
    "location": "Santa Fe Indian School",
    "number_of_students": "25",
    "teaching_tenure_years": "5 years",
    "percentage_of_girls": "48%",
    "percentage_of_boys": "52%",
    "attendance_percentage": "92%",
    "grade_level_competence": "mixed, ranging from 6th to 9th grade level",
    "classroom_challenges": "varying levels of mathematical preparedness, engagement during abstract concepts"
}

test_form_data_with_transcript = {
    **test_form_data,
    "lecture_transcript": """
    Today we're going to learn about linear equations. A linear equation is an equation where the highest power of the variable is 1.
    Let's start with the basic form: y = mx + b
    Here, 'm' is the slope and 'b' is the y-intercept.
    """
}

def test_generate_lecture_plan():
    """Test the lecture plan generation endpoint"""
    response = client.post("/generate-lecture-plan", json=test_form_data)
    
    # Check status code
    assert response.status_code == 200
    
    # Check response structure
    json_response = response.json()
    assert "status" in json_response
    assert "data" in json_response
    assert "lecture_plan" in json_response["data"]
    
    # Check content
    lecture_plan = json_response["data"]["lecture_plan"]
    assert isinstance(lecture_plan, str)
    assert len(lecture_plan) > 0
    
    # Check if response contains expected sections
    expected_sections = [
        "SUBTOPICS BREAKDOWN",
        "ENGAGEMENT STRATEGIES",
        "DIFFERENTIATION STRATEGIES",
        "TIMING AND PACING"
    ]
    for section in expected_sections:
        assert section in lecture_plan, f"Missing section: {section}"

def test_generate_feedback():
    """Test the feedback generation endpoint"""
    response = client.post("/generate-feedback", json=test_form_data_with_transcript)
    
    # Check status code
    assert response.status_code == 200
    
    # Check response structure
    json_response = response.json()
    assert "status" in json_response
    assert "data" in json_response
    assert "feedback" in json_response["data"]
    
    # Check content
    feedback = json_response["data"]["feedback"]
    assert isinstance(feedback, str)
    assert len(feedback) > 0
    
    # Check if response contains expected domains
    expected_domains = [
        "DOMAIN 1: PLANNING AND PREPARATION",
        "DOMAIN 2: CLASSROOM ENVIRONMENT",
        "DOMAIN 3: INSTRUCTION"
    ]
    for domain in expected_domains:
        assert domain in feedback, f"Missing domain: {domain}"

def test_generate_feedback_without_transcript():
    """Test feedback generation without transcript (should fail)"""
    response = client.post("/generate-feedback", json=test_form_data)
    assert response.status_code == 400
    assert "Lecture transcript is required" in response.json()["detail"]

def test_invalid_request():
    """Test with invalid data"""
    invalid_data = {"invalid": "data"}
    response = client.post("/generate-lecture-plan", json=invalid_data)
    assert response.status_code == 422  # Validation error

if __name__ == "__main__":
    pytest.main(["-v", "test_api.py"]) 