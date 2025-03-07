import streamlit as st
from pydantic import BaseModel
import sys
import os
import json

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from crews.learning_crew.learning_crew import LearningCrew


# Simplified UserProfile model
class UserProfile(BaseModel):
    current_level: str
    reading_sheet_music: str
    frequency_of_practice: str
    time_commitment: str
    goals: str = ""  # Optional field with default value

# Streamlit UI to collect user input
st.title("AI Piano Teacher 🎹")

with st.form(key="user_profile_form"):
    # Simplified form with only essential inputs
    current_level = st.selectbox("What is your current piano level?", 
                                ["Beginner", "Intermediate", "Advanced"])
    
    reading_sheet_music = st.selectbox("How comfortable are you reading sheet music?", 
                                      ["Beginner", "Intermediate", "Advanced"])
    
    frequency_of_practice = st.selectbox("How often can you practice?", 
                                        ["Once a week", "A few times a week", "Daily"])
    
    time_commitment = st.selectbox("How much time can you commit to each practice session?", 
                                  ["Less than 15 min", "15-30 min", "30-60 min", "More than 60 min"])
    
    # Optional field for goals
    goals = st.text_area("What are your goals in learning piano? (Optional)", "")

    submit_button = st.form_submit_button("Create My Piano Learning Plan")

# When the form is submitted, process the input and start the AI crew
if submit_button:
    with st.spinner("Creating your personalized piano learning plan..."):
        user_profile = UserProfile(
            current_level=current_level,
            reading_sheet_music=reading_sheet_music,
            frequency_of_practice=frequency_of_practice,
            time_commitment=time_commitment,
            goals=goals
        )
        
        # Initialize the learning crew and kickoff
        learning_crew = LearningCrew()
        result = learning_crew.crew().kickoff(inputs=user_profile.dict())

        
        # Display the AI-generated response in sections
        st.subheader("Your AI-Powered Piano Learning Journey 🎼")
        
        # Get the tasks output list
        tasks_output = result.tasks_output
        
        # Display each task's output as it appears in the terminal
        with st.expander("🧠 User Profile Analysis", expanded=True):
            st.markdown(tasks_output[0].raw)
        
        with st.expander("📝 Personalized Learning Plan", expanded=True):
            st.markdown(tasks_output[1].raw)
        
        with st.expander("🎵 Music Theory Concepts", expanded=True):
            st.markdown(tasks_output[2].raw)
        
        with st.expander("❓ Knowledge Quiz", expanded=True):
            st.markdown(tasks_output[3].raw)