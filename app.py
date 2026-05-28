import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Andrew & Stephanie Hawaii AI Planner", page_icon="🌺", layout="centered")

st.title("🌺 Andrew & Stephanie's Hawaii AI Planner")
st.write("Plan a Hawaii trip around the Honolulu wedding and Delta flights from Seattle.")

st.info(
    "Wedding anchor dates: October 7, 8, and 9 in Honolulu, Oahu. "
    "You must be in Honolulu for these dates."
)

st.subheader("Trip Basics")

island_hopping = st.selectbox(
    "Island plan",
    ["Not Sure - Recommend", "Oahu Only", "Two Islands", "Three Islands"]
)

before_wedding_days = st.slider("Days before the wedding", 0, 10, 3)
after_wedding_days = st.slider("Days after the wedding", 0, 10, 3)

budget = st.selectbox("Budget", ["Budget", "Moderate", "Luxury"])

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

st.subheader("Flight Details")

home_airport = st.text_input("Andrew's home airport", "SEA")
stephanie_airport = st.text_input("Stephanie's home airport", "SYR")

flight_preference = st.selectbox(
    "Flight preference",
    [
        "Delta flights only where possible",
        "Delta preferred but allow partners if needed",
        "Best schedule with Delta focus",
        "Use miles if possible"
    ]
)

st.caption(
    "Note: This app does not pull live Delta prices yet. It creates a Delta-focused flight strategy "
    "that should be verified on Delta.com or Google Flights."
)

if st.button("Create Our Hawaii Trip Plan"):

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    total_days = before_wedding_days + 3 + after_wedding_days

    prompt = f"""
    Create a Hawaii vacation plan for Andrew and his girlfriend Stephanie.

    IMPORTANT WEDDING DETAILS:
    - Wedding events are in Honolulu, Oahu.
    - Wedding dates are October 7, October 8, and October 9.
    - Andrew and Stephanie must be in Honolulu/Oahu for those three dates.
    - Keep wedding days mostly open and do not over-schedule them.

    PEOPLE / FLIGHT DETAILS:
    - Andrew starts from Seattle: {home_airport}
    - Stephanie starts from Syracuse, New York: {stephanie_airport}
    - Stephanie will fly round trip from Syracuse to Seattle before and after the Hawaii trip.
    - Andrew and Stephanie want to fly together from Seattle to Hawaii.
    - Hawaii flights should be Delta-focused.
    - Flight preference: {flight_preference}

    TRIP DETAILS:
    - Days before wedding: {before_wedding_days}
    - Wedding days: 3
    - Days after wedding: {after_wedding_days}
    - Total Hawaii trip length: {total_days} days
    - Island hopping preference: {island_hopping}
    - Budget: {budget}
    - Vacation style: {vibe}
    - Notes: {notes}

    PLEASE INCLUDE:

    1. Recommended total trip dates using October 7-9 as fixed wedding dates.
    2. Suggested Stephanie flight plan:
       - Syracuse to Seattle before Hawaii
       - Seattle to Syracuse after Hawaii
       - Include timing advice so she is not rushed.
    3. Delta-focused Seattle to Hawaii flight strategy:
       - SEA to HNL for the wedding portion
       - Mention likely Delta nonstop or connecting strategy
       - If island hopping is recommended, include realistic inter-island travel notes.
       - Clearly say that exact flight times and prices must be verified on Delta.com.
    4. Whether they should stay only on Oahu or visit multiple islands.
    5. Best island sequence before and after the wedding.
    6. Day-by-day itinerary.
    7. Wedding-day suggestions that are light and realistic.
    8. Romantic ideas for Andrew and Stephanie.
    9. Restaurant ideas.
    10. Hidden gems.
    11. Budget estimate.
    12. Packing list.
    13. Final recommendation on the ideal number of days before and after the wedding.

    Make it practical, romantic, impressive, and not too rushed.
    """

    with st.spinner("Planning Andrew and Stephanie's Hawaii trip..."):
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

    st.subheader("🌴 Your AI Hawaii Trip Plan")
    st.markdown(response.output_text)
