import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate


load_dotenv()


st.set_page_config(page_title="✈️ AI Travel Planner for Students", page_icon="✈️")
st.title("✈️ AI Trip Planner")
st.caption("Plan your perfect trip on a budget!")
load_dotenv()
if "GOOGLE_API_KEY" not in os.environ:
    st.error("Error: GOOGLE_API_KEY not found in environment variables.")
    st.stop()

model = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.8)
template_string = """
You are an expert travel planner specializing in creating exciting, budget-friendly itineraries for students.
Your tone should be witty, helpful, and encouraging.

Create a detailed, day-by-day travel plan based on the user's request.
Incorporate their specific interests and budget. For each day, suggest specific activities,
sights, and affordable food options. Prioritize free activities and mention any known student discounts.
Give the trip a fun and creative title!

**User's Trip Details:**
- **Destination:** {destination}
- **Duration:** {days} days
- **Budget:** {budget}
- **Interests:** {interests}

Begin the itinerary now.
"""
prompt_template = PromptTemplate.from_template(template_string)

with st.form("trip_form"):
    st.header("Please provide your trip details:")
    destination_input = st.text_input("📍 Please write the location for the trip:")
    days_input = st.text_input("⏳ How many days will your trip be?")
    budget_input = st.text_input("💰 What is your budget?")
    interests_input = st.text_area("🎨 What are your interests? (e.g., hiking, art museums, street food)")
    
    submitted = st.form_submit_button("Generate Trip Plan")
if submitted:
    if all([destination_input, days_input, budget_input, interests_input]):
        with st.spinner("Crafting your personalized adventure... 🗺️"):
            try:
                formatted_prompt = prompt_template.format(
                    destination=destination_input,
                    days=days_input,
                    budget=budget_input,
                    interests=interests_input
                )       
                response = model.invoke(formatted_prompt)
                st.subheader("🎉 Here's Your Custom Itinerary!")
                st.markdown(response.content)

            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please fill out all the fields to generate a plan.")
