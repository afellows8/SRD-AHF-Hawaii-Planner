import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="Andrew & Stephanie Hawaii AI Planner",
    page_icon="🌺",
    layout="centered"
)

st.image(
    "Spain Picture.jpg",
    caption="Barcelona, Spain 🇪🇸 — planning the next adventure",
    use_container_width=True
)

st.title("🌺 Andrew & Stephanie's Hawaii AI Planner")

st.markdown(
    """
    Planning our Hawaii adventure around the Honolulu wedding
    on October 7–9 while optimizing Delta flights, island hopping,
    romance, food, and relaxation.
    """
)

st.info(
    "Wedding anchor dates: October 7, 8, and 9 in Honolulu, Oahu. "
    "We must be in Honolulu for these dates."
)

st.subheader("Trip Basics")

island_hopping = st.selectbox(
    "Island plan",
    ["Not Sure - Recommend", "Oahu Only", "Two Islands", "Three Islands"]
)

before_wedding_days = st.slider("Days before the wedding in Hawaii", 0, 10, 3)
after_wedding_days = st.slider("Days after the wedding in Hawaii", 0, 10, 3)

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

st.write(
    "Stephanie will fly round trip from Syracuse to Seattle. "
    "Then Andrew and Stephanie will fly together round trip from Seattle to Hawaii."
)

flight_preference = st.selectbox(
    "Flight preference",
    [
        "Delta flights only where possible",
        "Delta preferred but allow partners if needed",
        "Best schedule with Delta focus",
        "Use miles if possible"
    ]
)

if st.button("Create Our Hawaii Trip Plan"):

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    total_hawaii_days = before_wedding_days + 3 + after_wedding_days

    prompt = f"""
    Create a Hawaii vacation plan for Andrew and Stephanie.

    IMPORTANT WEDDING DETAILS:
    - Wedding events are in Honolulu, Oahu.
    - Wedding dates are October 7, October 8, and October 9.
    - Andrew and Stephanie must be in Honolulu/Oahu for those three dates.
    - Keep wedding days mostly open and realistic.

    TRAVEL LOGISTICS:
    - Andrew lives in Seattle and departs from SEA.
    - Stephanie lives in Syracuse, New York and departs from SYR.
    - Stephanie will fly round trip from Syracuse to Seattle.
    - Andrew and Stephanie will then fly together round trip from Seattle to Hawaii.
    - Hawaii flights should be Delta-focused.
    - Flight preference: {flight_preference}

    TRIP DETAILS:
    - Days before wedding in Hawaii: {before_wedding_days}
    - Wedding days: 3
    - Days after wedding in Hawaii: {after_wedding_days}
    - Total Hawaii trip length: {total_hawaii_days} days
    - Island hopping preference: {island_hopping}
    - Budget: {budget}
    - Vacation style: {vibe}
    - Notes: {notes}

    PLEASE INCLUDE:

    1. Recommended total trip dates using October 7-9 as fixed wedding dates.
    2. Stephanie's flight strategy:
       - Syracuse to Seattle before Hawaii
       - Seattle to Syracuse after Hawaii
       - Timing advice so she is not rushed.
    3. Andrew and Stephanie's Delta-focused Hawaii flight strategy:
       - Seattle to Hawaii
       - Hawaii back to Seattle
       - Mention that exact Delta flight times and prices need to be verified on Delta.com.
    4. Whether they should stay only on Oahu or visit multiple islands.
    5. Best island sequence before and after the wedding.
    6. Realistic inter-island travel notes.
    7. Day-by-day itinerary.
    8. Light wedding-day suggestions.
    9. Romantic ideas for Andrew and Stephanie.
    10. Restaurant ideas.
    11. Hidden gems.
    12. Budget estimate.
    13. Packing list.
    14. Final recommendation on the ideal number of days before and after the wedding.

    The plan should feel like a thoughtful trip designed specifically for Andrew and Stephanie as a couple,
    balancing romance, adventure, food, relaxation, Delta flights, and wedding obligations.

    Make it practical, romantic, impressive, and not too rushed.
    """

    with st.spinner("Planning Andrew and Stephanie's Hawaii trip..."):
        response = client.responses.create(
            model="gpt-5-nano",
            input=prompt
        )

    st.subheader("🌴 Your AI Hawaii Trip Plan")
    st.markdown(response.output_text)
