import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="Andrew & Stephanie Hawaii AI Planner",
    page_icon="🌺",
    layout="centered"
)

# Header Image
st.image(
    "SRDAHF.png",
    caption="Andrew & Stephanie 🌺",
    use_container_width=True
)

# Title
st.title("🌺 Andrew & Stephanie's Hawaii AI Planner")

st.markdown("""
Planning our Hawaii adventure around the Honolulu wedding
on October 7-9 while optimizing Delta flights, island hopping,
romance, food, relaxation, and adventure.
""")

# Wedding Info
st.info(
    "Wedding dates are October 7, 8, and 9 in Honolulu, Oahu. "
    "The itinerary should keep us in Honolulu for those dates."
)

# Trip Settings
st.subheader("✈️ Trip Planning")

island_hopping = st.selectbox(
    "Island Plan",
    [
        "Not Sure - Recommend",
        "Oahu Only",
        "Two Islands",
        "Three Islands"
    ]
)

before_wedding_days = st.slider(
    "Days in Hawaii BEFORE the wedding",
    0,
    10,
    3
)

after_wedding_days = st.slider(
    "Days in Hawaii AFTER the wedding",
    0,
    10,
    4
)

budget = st.selectbox(
    "Budget",
    [
        "Budget",
        "Moderate",
        "Luxury"
    ]
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
        "Beaches",
        "Luxury",
        "Culture",
        "Nightlife"
    ],
    default=[
        "Romantic",
        "Food",
        "Beaches"
    ]
)

notes = st.text_area(
    "Additional Notes",
    "We want an amazing romantic trip that balances relaxation, adventure, great food, and wedding obligations."
)

# Flight Section
st.subheader("🛫 Flight Preferences")

flight_preference = st.selectbox(
    "Flight Preference",
    [
        "Delta Only",
        "Delta Preferred",
        "Use SkyMiles If Possible",
        "Best Delta Schedule"
    ]
)

if st.button("🌴 Create Our Hawaii Trip Plan"):

    client = OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"]
    )

    total_hawaii_days = (
        before_wedding_days
        + 3
        + after_wedding_days
    )

    prompt = f"""
Create a personalized Hawaii vacation plan for Andrew and Stephanie.

ABOUT US:
- Andrew lives in Seattle.
- Stephanie lives in Syracuse, New York.
- Stephanie will fly Syracuse -> Seattle before Hawaii.
- Andrew and Stephanie will then fly together Seattle -> Hawaii.
- After Hawaii they will fly together Hawaii -> Seattle.
- Stephanie will then fly Seattle -> Syracuse.

WEDDING DETAILS:
- Wedding events are October 7, 8, and 9.
- Wedding location is Honolulu, Oahu.
- We must be in Honolulu for those dates.
- Keep wedding days relatively open.

TRIP DETAILS:
- Days before wedding: {before_wedding_days}
- Days after wedding: {after_wedding_days}
- Total Hawaii days: {total_hawaii_days}
- Island plan: {island_hopping}
- Budget: {budget}
- Vacation style: {vibe}
- Notes: {notes}

FLIGHT PREFERENCES:
- {flight_preference}
- Focus on Delta Airlines.
- Suggest realistic Delta routing.
- Suggest the best timing for Stephanie's Syracuse-Seattle flights.
- Suggest the best timing for our Seattle-Hawaii flights.
- Mention that live schedules and fares should be verified directly with Delta.

PLEASE PROVIDE:

1. Three trip options:
   - Short trip
   - Medium trip
   - Longer trip

2. Recommended option and why.

3. Best island combination.

4. Detailed day-by-day itinerary.

5. Romantic experiences.

6. Great restaurants.

7. Hidden gems.

8. Budget estimate.

9. Packing list.

10. Suggested flight strategy.

11. Whether we should spend more days before or after the wedding.

Make the trip feel special, romantic, memorable, practical, and optimized around the wedding.
"""

    with st.spinner("Planning Andrew & Stephanie's Hawaii adventure..."):

        response = client.responses.create(
            model="gpt-5-nano",
            input=prompt
        )

    st.success("Trip plan complete!")

    st.subheader("🌺 Your Hawaii Plan")

    st.markdown(response.output_text)
