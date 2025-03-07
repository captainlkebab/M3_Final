import streamlit as st
from pydantic import BaseModel
import sys
import os
import json

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from crews.learning_crew.learning_crew import LearningCrew

# Define the UserProfile model
class UserProfile(BaseModel):
    motivation: str
    goals: str
    previous_experience: str
    reading_sheet_music: str
    scales_chords_intervals: str
    finger_exercises_and_scales: str
    pieces_played_before: str
    frequency_of_practice: str
    time_commitment: str

# Streamlit UI to collect user input
st.title("AI Piano Teacher 🎹")

with st.form(key="user_profile_form"):
    # Form inputs remain unchanged
    motivation = st.text_area("What motivates you to learn piano?")
    goals = st.text_area("What are your goals in learning piano?")
    previous_experience = st.selectbox("Do you have any previous experience playing the piano?", ["None", "Beginner", "Intermediate", "Advanced"])
    reading_sheet_music = st.selectbox("Can you read sheet music?", ["Not at all", "A little", "Comfortable", "Fluent"])
    scales_chords_intervals = st.selectbox("Do you understand scales, chords, and intervals?", ["Not at all", "Somewhat", "Yes"])
    finger_exercises_and_scales = st.selectbox("Have you practiced finger exercises and scales before?", ["Never", "Occasionally", "Regularly"])
    pieces_played_before = st.text_area("What pieces have you played before (if any)?")
    frequency_of_practice = st.selectbox("How often do you practice?", ["Rarely", "Once a week", "A few times a week", "Daily"])
    time_commitment = st.selectbox("How much time can you commit to practicing per session?", ["Less than 15 min", "15-30 min", "30-60 min", "More than 1 hour"])

    submit_button = st.form_submit_button("Start My Lesson!")

# When the form is submitted, process the input and start the AI crew
if submit_button:
    with st.spinner("Creating your personalized piano learning plan..."):
        user_profile = UserProfile(
            motivation=motivation,
            goals=goals,
            previous_experience=previous_experience,
            reading_sheet_music=reading_sheet_music,
            scales_chords_intervals=scales_chords_intervals,
            finger_exercises_and_scales=finger_exercises_and_scales,
            pieces_played_before=pieces_played_before,
            frequency_of_practice=frequency_of_practice,
            time_commitment=time_commitment,
        )

        # Initialize the learning crew and kickoff
        learning_crew = LearningCrew()
        result = learning_crew.crew().kickoff(inputs=user_profile.dict())
        
        # Get the raw result
        raw_result = result.raw if hasattr(result, 'raw') else result
        
    # Display the AI-generated response in sections
    st.subheader("Your AI-Powered Piano Learning Journey 🎼")
    
    # Create a more organized display of results with expandable sections
    with st.expander("🧠 User Profile Analysis", expanded=True):
        try:
            profile_analysis = result["analyze_user_profile"]
            st.markdown(profile_analysis)
        except:
            st.write("Could not retrieve user profile analysis.")
    
    with st.expander("📝 Personalized Learning Plan", expanded=True):
        try:
            learning_plan = result["create_learning_plan"]
            st.markdown(learning_plan)
            
            # If the learning plan contains a structured weekly plan, display it nicely
            if "Week 1" in learning_plan:
                st.subheader("Weekly Breakdown")
                weeks = learning_plan.split("Week")
                for i, week in enumerate(weeks[1:], 1):
                    with st.expander(f"Week {i}", expanded=i==1):
                        st.markdown(f"Week{week}")
        except:
            st.write("Could not retrieve learning plan.")
    
    with st.expander("🎵 Music Theory Concepts", expanded=True):
        try:
            music_theory = result["explain_music_theory"]
            st.markdown(music_theory)
        except:
            st.write("Could not retrieve music theory explanation.")
    
    with st.expander("❓ Knowledge Quiz", expanded=True):
        try:
            quiz = result["create_quiz"]
            
            # Display the quiz in a more interactive way
            st.markdown("### Test Your Understanding")
            
            # Split the quiz into questions
            if "Q1:" in quiz:
                questions = quiz.split("Q")
                for i, question in enumerate(questions[1:], 1):
                    with st.expander(f"Question {i}", expanded=False):
                        st.markdown(f"Q{question}")
            else:
                st.markdown(quiz)
        except:
            st.write("Could not retrieve quiz.")
    
    # Add a download button for the complete plan
    st.download_button(
        label="Download Complete Learning Plan",
        data=raw_result,
        file_name="piano_learning_plan.txt",
        mime="text/plain"
    )