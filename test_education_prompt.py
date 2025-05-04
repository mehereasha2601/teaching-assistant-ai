from openai_integration import OpenAIIntegration

def test_education_prompt():
    print("Testing Educational Feedback Prompt...")
    
    # Create instance of OpenAIIntegration
    ai = OpenAIIntegration()
    
    # Sample data for testing
    test_data = {
        "grade": "8th",
        "topic": "Algebra - Linear Equations",
        "country": "United States",
        "location": "Santa Fe Indian School",
        "number_of_students": "25",
        "percentage_of_girls": "48%",
        "percentage_of_boys": "52%",
        "attendance_percentage": "92%",
        "grade_level_competence": "mixed, ranging from 6th to 9th grade level",
        "teaching_tenure_years": "5 years",
        "classroom_challenges": "varying levels of mathematical preparedness, engagement during abstract concepts, and maintaining consistent attendance",
        "lecture_transcript": """
        Today we're going to learn about linear equations. Linear equations are mathematical expressions that create straight lines when graphed. They follow the general form y = mx + b, where:
        - m represents the slope of the line
        - b represents the y-intercept
        - x and y are variables

        Let's look at an example: y = 2x + 3
        In this equation:
        - The slope (m) is 2, which means for every unit we move right on the x-axis, we move up 2 units on the y-axis
        - The y-intercept (b) is 3, which means the line crosses the y-axis at point (0,3)

        To graph this line:
        1. Start at the y-intercept (0,3)
        2. Use the slope to find the next point: move right 1 unit, up 2 units
        3. Connect the points to form the line

        Now, let's learn how to solve linear equations. Take the equation: 2x + 3 = 7
        Steps to solve:
        1. Isolate the variable term (2x) by subtracting 3 from both sides
        2. Divide both sides by 2 to solve for x
        3. Check your answer by substituting back into the original equation

        Key points to remember:
        - Linear equations always graph as straight lines
        - The slope tells us how steep the line is
        - The y-intercept tells us where the line crosses the y-axis
        - When solving, always perform the same operation on both sides of the equation
        """
    }
    
    # Format the prompt with test data
    prompt = f"""
    We are teaching grade {test_data['grade']} the topic {test_data['topic']} in {test_data['country']}. 
    My class is based out of {test_data['location']}. There are {test_data['number_of_students']} in my class, 
    {test_data['percentage_of_girls']} of girls and {test_data['percentage_of_boys']} of boys.
    The attendance is expected to be {test_data['attendance_percentage']}, and the grade level competence 
    of my students is {test_data['grade_level_competence']}. I have been teaching this grade for 
    {test_data['teaching_tenure_years']}. The challenges I face are usually {test_data['classroom_challenges']}. 
    
    Below is the transcript of my recent lecture. Please provide specific, actionable feedback based on the actual content of this lecture.
    For each point below, provide:
    1. A specific observation from the lecture
    2. A concrete suggestion for improvement
    3. An example of how to implement the suggestion

    LECTURE TRANSCRIPT:
    {test_data['lecture_transcript']}
    
    Please provide feedback for EACH of the following points:

    DOMAIN 1: PLANNING AND PREPARATION
    1. Lecture Sequence: How well does the lecture sequence build understanding of linear equations?
    2. Mixed Ability Levels: Are the examples and explanations appropriate for the mixed ability levels?
    3. Key Concepts: How effectively are key concepts introduced and connected?
    4. Misconceptions: What specific misconceptions might students have about linear equations?
    5. Lesson Structure: How could the lesson be better structured for different learning levels?

    DOMAIN 2: CLASSROOM ENVIRONMENT
    1. Student Engagement: How can the lecture be made more engaging for students with varying mathematical abilities?
    2. Attention Maintenance: What specific strategies could be used to maintain student attention during abstract concepts?
    3. Content Relevance: How can the content be made more relevant to students' lives?
    4. Interactive Learning: What specific activities could be added to make the learning more interactive?
    5. Learning Styles: How can the lecture better accommodate different learning styles?

    DOMAIN 3: INSTRUCTION
    1. Problem-Solving Steps: How effectively are the steps for solving linear equations explained?
    2. Visual Aids: What specific visual aids or examples could enhance understanding?
    3. Concept Explanation: How could the explanation of slope and y-intercept be improved?
    4. Practice Opportunities: What specific practice opportunities could be added?
    5. Differentiated Instruction: How could the lecture better address the needs of students at different grade levels?

    For each point above, provide specific examples and concrete suggestions that can be implemented immediately in the classroom.
    """
    
    print("\nSending prompt to OpenAI...")
    response = ai.get_response(prompt)
    
    if response:
        print("\nResponse received successfully!")
        print("\nFeedback from OpenAI:\n")
        print(response)
    else:
        print("Failed to get response from OpenAI")
        print("Please check your API key and internet connection.")

if __name__ == "__main__":
    test_education_prompt() 