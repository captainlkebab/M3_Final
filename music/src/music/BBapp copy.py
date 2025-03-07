import streamlit as st
import sys
import os

# Add the src directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Now Python can find the music module
from music.main import kickoff
from pydantic import BaseModel

# 🟢 Define the User Input Form Model
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

# 🟢 Streamlit UI
st.title("🎵 AI Music Teacher")
st.write("Enter your details and let AI generate a personalized music learning plan!")

# Collect user input
with st.form("user_input_form"):
    motivation = st.text_area("What motivates you to learn music?")
    goals = st.text_area("What are your goals in learning music?")
    previous_experience = st.selectbox("Your experience level:", ["Beginner", "Intermediate", "Advanced"])
    reading_sheet_music = st.selectbox("Can you read sheet music?", ["Yes", "No", "Somewhat"])
    scales_chords_intervals = st.selectbox("Do you understand scales, chords, and intervals?", ["Yes", "No", "Somewhat"])
    finger_exercises_and_scales = st.selectbox("Do you practice finger exercises and scales?", ["Yes", "No", "Sometimes"])
    pieces_played_before = st.text_area("What pieces have you played before?")
    frequency_of_practice = st.selectbox("How often do you practice?", ["Daily", "A few times a week", "Rarely"])
    time_commitment = st.selectbox("How much time can you dedicate to practice?", ["Less than 30 minutes", "30-60 minutes", "More than an hour"])
    
    submit_button = st.form_submit_button("Start Learning")

# 🟢 When User Submits Input
if submit_button:
    # ✅ Convert user input into a dictionary (must match LearningFlow expected state)
    user_profile = {
        "motivation": motivation,
        "goals": goals,
        "previous_experience": previous_experience,
        "reading_sheet_music": reading_sheet_music,
        "scales_chords_intervals": scales_chords_intervals,
        "finger_exercises_and_scales": finger_exercises_and_scales,
        "pieces_played_before": pieces_played_before,
        "frequency_of_practice": frequency_of_practice,
        "time_commitment": time_commitment,
    }

    st.write("🚀 AI is analyzing your music profile and creating a learning plan...")
    
    # Call kickoff without arguments
        # ✅ Pass the structured user input to `kickoff`
    with st.spinner("Generating your learning plan..."):
        result = kickoff(user_profile)  # Pass user input
        st.success("Here is your personalized learning plan:")
        st.write(result)