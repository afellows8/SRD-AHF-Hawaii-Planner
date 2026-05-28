import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Hawaii AI Planner", page_icon="🌺")

st.title("🌺 Hawaii AI Planner")
st.write("Create a personalized Hawaii vacation with AI.")

island = st.selectbox(
    "Which island?",
    ["Oahu", "Maui", "Kauai", "Big Island", "Not Sure"]
)

days = st.number_input("Trip Length (Days)", 3, 21, 7)

budget = st.selectbox(
    "Budget",
    ["Budget", "Moderate", "Luxury"]
)

vibe = st.multiselect(
    "Vacation Style",
    [
        "Romantic",
        "Adventure",
        "Food",
        "Relaxation",
        "Hiking",
        "Snorkeling",
        "Luxury"
    ]
)

notes = st.text_area(
    "Anything special?",
    "We love beaches, seafood, and sunsets."
)

if st.button("Create My Hawaii Trip"):

    client = OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"]
    )

    prompt = f"""
    Create a Hawaii vacation plan.

    Island: {island}
    Length: {days} days
    Budget: {budget}
    Style: {vibe}
    Notes: {notes}

    Include:

    - Day by day itinerary
    - Best restaurants
    - Romantic ideas
    - Hidden gems
    - Budget estimate
    - Packing list

    Make it fun and detailed.
    """

    with st.spinner("Planning your trip..."):
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

    st.markdown(response.output_text)
