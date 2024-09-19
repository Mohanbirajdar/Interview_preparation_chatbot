import streamlit as st
import google.generativeai as genai

# Configure the API key for Generative AI
genai.configure(api_key="GOOGLE_API_KEY")

# Function to generate interview questions
def generate_interview_question(domain, level):
    prompt = f"Generate a {level} interview question for a candidate applying for {domain}."
    response = get_gemini_response(model="models/gemini-1.5-tuned", messages=[{"content": prompt}])
    return response['candidates'][0]['content']

# Function to provide feedback and improvement suggestions
def suggest_improvements(answer, feedback):
    prompt = f"Given this interview answer: '{answer}', and the feedback: '{feedback}', suggest improvements."
    response = get_gemini_response(model="models/gemini-1.5-tuned", messages=[{"content": prompt}])
    return response['candidates'][0]['content']

# Start the Streamlit app
st.title("Interview Preparation Chatbot")

# Choose interview domain
domain = st.selectbox("Choose the domain for the interview", ["Software Development", "Data Science", "Marketing", "Management"])

# Choose the level of difficulty
level = st.selectbox("Choose the question difficulty level", ["Beginner", "Intermediate", "Advanced"])

# Button to start interview
if st.button("Start Interview"):
    st.session_state["questions_asked"] = 0

if "questions_asked" not in st.session_state:
    st.session_state["questions_asked"] = 0

if st.session_state["questions_asked"] >= 1:
    # Display a question
    question = generate_interview_question(domain, level)
    st.write(f"Q{st.session_state['questions_asked']}: {question}")
    
    # Get user's answer
    user_answer = st.text_input("Your Answer")

    if user_answer:
        # Get feedback from user
        feedback = st.selectbox("How did you find this question?", ["Easy", "Moderate", "Difficult", "Irrelevant"])
        
        # Suggest improvements based on user's answer and feedback
        if st.button("Submit Feedback and Improve"):
            improvement_suggestion = suggest_improvements(user_answer, feedback)
            st.write("Improvement Suggestions:")
            st.write(improvement_suggestion)
            
        # Ask the next question
        if st.button("Next Question"):
            st.session_state["questions_asked"] += 1

else:
    if st.button("Ask First Question"):
        st.session_state["questions_asked"] = 1

