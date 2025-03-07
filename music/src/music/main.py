#!/usr/bin/env python
from random import randint
from pydantic import BaseModel
from crewai.flow import Flow, listen, start
from music.crews.learning_crew.learning_crew import LearningCrew
from dotenv import load_dotenv

load_dotenv()


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


# class LearningFlow(Flow[PoemState]):
class LearningFlow(Flow[UserProfile]):
    state: UserProfile

    @start()
    def generate_user_profile(self):
        """Analyze user profile"""
        print("🚀 Analyzing user profile...")

        # Run the Crew with user input
        result = LearningCrew().crew().kickoff(inputs=self.state.dict())

        # Store the entire result for further steps
        self.state.learning = result  # Store CrewOutput

    @listen(generate_user_profile)
    def generate_learning_plan(self):
        """Generate a personalized learning plan"""
        print("📖 Generating Learning Plan...")

        # Extract learning plan from result
        learning_plan = self.state.learning["create_learning_plan"] if "create_learning_plan" in self.state.learning else "No output"

        print("✅ Learning Plan Generated:", learning_plan)
        self.state.learning = learning_plan  # Store plan

    @listen(generate_learning_plan)
    def save_learning(self):
        """Save learning plan to a file"""
        print("💾 Saving learning plan...")

        with open("learning.txt", "w") as f:
            f.write(self.state.learning)

    @listen(generate_learning_plan)
    def explain_music_theory(self):
        """Explain music theory concepts"""
        print("🎵 Explaining music theory...")

        music_theory = self.state.learning["explain_music_theory"] if "explain_music_theory" in self.state.learning else "No explanation available"
        print("🎼 Music Theory Explanation:", music_theory)
        
def kickoff(user_profile_data):
    """Start the learning flow with user profile data"""
    try:
        # Create a UserProfile instance from the input data
        user_profile = UserProfile(
            motivation=user_profile_data["motivation"],
            goals=user_profile_data["goals"],
            previous_experience=user_profile_data["previous_experience"],
            reading_sheet_music=user_profile_data["reading_sheet_music"],
            scales_chords_intervals=user_profile_data["scales_chords_intervals"],
            finger_exercises_and_scales=user_profile_data["finger_exercises_and_scales"],
            pieces_played_before=user_profile_data["pieces_played_before"],
            frequency_of_practice=user_profile_data["frequency_of_practice"],
            time_commitment=user_profile_data["time_commitment"],
            learning={}  # Initialize with empty dict
        )
        
        # Initialize LearningFlow with the user profile as state
        learning_flow = LearningFlow(state=user_profile)
        
        # Start the flow
        result = learning_flow.kickoff()
        
        return result
    except Exception as e:
        print(f"Error in kickoff: {e}")
        raise
def plot():
    learning_flow = LearningFlow()
    learning_flow.plot()

if __name__ == "__main__":
    kickoff()
