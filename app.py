import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Hawaii AI Planner", page_icon="🌺", layout="centered")

st.title("🌺 Hawaii AI Planner")
st.write("Plan our Hawaii trip around the Honolulu wedding on October 7, 8, and 9.")

st.info(
    "Wedding anchor dates: October 7, 8, and 9 in Honolulu, Oahu. "
    "The trip plan must keep us in Honolulu for those dates."
)

island = st.selectbox(
    "Main island preference",
    ["Not Sure - Recommend", "Oahu", "Maui", "Kauai", "Big Island"]
)

island_hopping = st.selectbox(
    "Island plan",
    ["Not Sure - Recommend", "One Island Only", "Two Islands", "Three Islands"]
)

before_wedding_days = st.slider(
    "Days before the wedding",
    0, 10, 3
)

after_wedding_days = st.slider(
    "Days after the wedding",
    0, 10, 3
)

budget = st.selectbox(
    "Budget",
    ["Budget", "Moderate", "Luxury"]
)

vibe = st.multiselect(
    "Vacation style",
    [
        "Romantic",
        "Adventure",
        "Food",
        "Relaxation",
        "Hiking",
        "Snorkeling",
        "Beaches",
        "Luxury",
        "Culture",
        "Nightlife"
    ],
    default=["Romantic", "Food", "Beaches"]
)

notes = st.text_area(
    "Anything special?",
    "We want this to feel romantic and memorable, but not overly rushed."
)

if st.button("Create Our Hawaii Trip Plan"):

    client = OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"]
    )

    total_days = before_wedding_days + 3 + after_wedding_days

    prompt = f"""
    Create a Hawaii vacation plan for a couple.

    IMPORTANT WEDDING DETAILS:
    - Wedding events are in Honolulu, Oahu.
    - Wedding dates are October 7, October 8, and October 9.
    - The couple must be in Honolulu/Oahu for those three dates.
    - Keep wedding days mostly open and do not over-schedule them.

    TRIP DETAILS:
    - Days before wedding: {before_wedding_days}
    - Wedding days: 3
    - Days after wedding: {after_wedding_days}
    - Total trip length: {total_days} days
    - Main island preference: {island}
    - Island hopping preference: {island_hopping}
    - Budget: {budget}
    - Vacation style: {vibe}
    - Notes: {notes}

    PLEASE INCLUDE:

    1. Recommended total trip dates using October 7-9 as the fixed wedding dates.
    2. Whether they should stay only on Oahu or visit multiple islands.
    3. Best island sequence before and after the wedding.
    4. Realistic inter-island travel timing.
    5. Day-by-day itinerary.
    6. Wedding-day suggestions that are light and realistic.
    7. Romantic ideas.
    8. Restaurant ideas.
    9. Hidden gems.
    10. Budget estimate.
    11. Packing list.
    12. A final recommendation on the ideal number of days to go before and after.

    Make it practical, romantic, impressive, and not too rushed.
    """

    with st.spinner("Planning your Hawaii trip..."):
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

    st.subheader("🌴 Your AI Hawaii Trip Plan")
    st.markdown(response.output_text)
