#!/usr/bin/env python
from pydantic import BaseModel
from crewai.flow import Flow, listen, start
from music.crews.learning_crew.learning_crew import LearningCrew
from dotenv import load_dotenv

load_dotenv()


class UserProfile(BaseModel):
    current_level: str
    reading_sheet_music: str
    frequency_of_practice: str
    time_commitment: str
    goals: str = ""


class LearningFlow(Flow[UserProfile]):
    state: UserProfile

    @start()
    def generate_user_profile(self):
        """Analyze user profile"""
        print("🚀 Analyzing user profile...")

        # Run the Crew with user input
        result = LearningCrew().crew().kickoff(inputs=self.state.dict())
        
        # Store the entire result for further steps
        self.state.learning = result

    @listen(generate_user_profile)
    def generate_learning_plan(self):
        """Generate a personalized learning plan"""
        print("📖 Generating Learning Plan...")

        # Extract learning plan from tasks output
        if hasattr(self.state.learning, 'tasks_output'):
            learning_plan = self.state.learning.tasks_output[1].raw
        else:
            learning_plan = "No learning plan available"

        print("✅ Learning Plan Generated:", learning_plan)
        self.state.learning_plan = learning_plan

    @listen(generate_learning_plan)
    def get_user_week_selection(self):
        """Get user input on which week to focus on"""
        print("🗓️ Please select a week from the learning plan...")
        
        # Display available weeks
        print("Available weeks from your learning plan:")
        print("1: Week 1  2: Week 2  3: Week 3  4: Week 4")
        print("5: Week 5  6: Week 6  7: Week 7  8: Week 8")
        print("9: Week 9  10: Week 10  11: Week 11  12: Week 12")
        
        # Get user input
        selected_week = input("Enter the week number (1-12): ")
        
        # Store the selected week
        self.state.selected_week = selected_week
        print(f"✅ Selected Week {selected_week}")

    @listen(get_user_week_selection)
    def explain_music_theory(self):
        """Explain music theory concepts for the selected week"""
        print(f"🎵 Explaining music theory for Week {self.state.selected_week}...")

        # Extract music theory from tasks output
        if hasattr(self.state.learning, 'tasks_output'):
            music_theory = self.state.learning.tasks_output[2].raw
            
            # You could potentially filter the content based on the selected week here
            # This would require parsing the music theory content
            
        else:
            music_theory = "No music theory explanation available"

        print("🎼 Music Theory Explanation:", music_theory)
        self.state.music_theory = music_theory

    @listen(explain_music_theory)
    def create_quiz(self):
        """Create a quiz based on the material for the selected week"""
        print(f"❓ Creating quiz for Week {self.state.selected_week}...")
        
        # Extract quiz from tasks output
        if hasattr(self.state.learning, 'tasks_output'):
            quiz = self.state.learning.tasks_output[3].raw
            
            # You could potentially filter the quiz based on the selected week here
            
        else:
            quiz = "No quiz available"

        print("📝 Quiz Created:", quiz)
        self.state.quiz = quiz


def kickoff(user_profile_data):
    """Start the learning flow with user profile data"""
    try:
        # Create a UserProfile instance from the input data
        user_profile = UserProfile(**user_profile_data)
        
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
