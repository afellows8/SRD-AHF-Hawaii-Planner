import streamlit as st
from openai import OpenAI
import csv
import io

st.set_page_config(
    page_title="Andrew & Stephanie Hawaii AI Planner",
    page_icon="🌺",
    layout="centered"
)

st.image(
    "SRDAHF.png",
    caption="Andrew & Stephanie 🌺",
    use_container_width=True
)

st.title("🌺 Andrew & Stephanie's Hawaii AI Planner")

st.markdown("""
Planning our Hawaii adventure around the Honolulu wedding
on October 7-9 with Delta flights, island hopping, romance,
food, activities, and real research links.
""")

st.info(
    "Wedding dates are October 7, 8, and 9 in Honolulu, Oahu. "
    "The itinerary should keep us in Honolulu for those dates."
)

st.subheader("✈️ Trip Planning")

island_count = st.selectbox(
    "How many islands would you like to visit?",
    [
        "Not Sure - Recommend",
        "One Island",
        "Two Islands",
        "Three Islands"
    ]
)

all_islands = ["Oahu", "Maui", "Kauai", "Big Island"]

selected_islands = []

if island_count == "One Island":
    selected_islands = st.multiselect(
        "Choose your island",
        all_islands,
        default=["Oahu"],
        max_selections=1
    )

elif island_count == "Two Islands":
    selected_islands = st.multiselect(
        "Choose two islands",
        all_islands,
        default=["Oahu", "Maui"],
        max_selections=2
    )

elif island_count == "Three Islands":
    selected_islands = st.multiselect(
        "Choose three islands",
        all_islands,
        default=["Oahu", "Maui", "Kauai"],
        max_selections=3
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
        "Beaches",
        "Luxury",
        "Culture",
        "Nightlife"
    ],
    default=["Romantic", "Food", "Beaches"]
)

must_do = st.text_area(
    "Things we absolutely want to do",
    "Snorkeling, great seafood, beach day, romantic sunset dinner"
)

notes = st.text_area(
    "Additional Notes",
    "We want an amazing romantic trip that balances relaxation, adventure, great food, and wedding obligations."
)

recommendation_style = st.selectbox(
    "Recommendation Style",
    [
        "Full AI Itinerary",
        "Links and Reviews Research Mode",
        "Both Itinerary and Research Links"
    ]
)

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

st.subheader("📌 Saved Ideas Board")

if "ideas" not in st.session_state:
    st.session_state.ideas = []

idea_name = st.text_input("Idea name", placeholder="Example: Sunset dinner at House Without A Key")
idea_category = st.selectbox(
    "Idea category",
    ["Activity", "Restaurant", "Beach", "Hotel Area", "Flight", "Romantic Idea", "Other"]
)
idea_notes = st.text_area("Idea notes", placeholder="Why we like it, price, link, location, etc.")

if st.button("Save Idea"):
    if idea_name.strip():
        st.session_state.ideas.append({
            "Idea": idea_name,
            "Category": idea_category,
            "Notes": idea_notes
        })
        st.success("Idea saved!")

if st.session_state.ideas:
    st.write("Saved ideas:")
    st.dataframe(st.session_state.ideas, use_container_width=True)

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["Idea", "Category", "Notes"])
    writer.writeheader()
    writer.writerows(st.session_state.ideas)

    st.download_button(
        label="Download Saved Ideas as CSV",
        data=output.getvalue(),
        file_name="andrew_stephanie_hawaii_ideas.csv",
        mime="text/csv"
    )

if st.button("🌴 Create Our Hawaii Trip Plan"):

    client = OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"]
    )

    total_hawaii_days = before_wedding_days + 3 + after_wedding_days

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
- Number of islands requested: {island_count}
- Selected islands: {selected_islands}
- Budget: {budget}
- Vacation style: {vibe}
- Things we absolutely want to do: {must_do}
- Notes: {notes}
- Recommendation style: {recommendation_style}

FLIGHT PREFERENCES:
- {flight_preference}
- Focus on Delta Airlines.
- Suggest realistic Delta routing.
- Suggest the best timing for Stephanie's Syracuse-Seattle flights.
- Suggest the best timing for Andrew and Stephanie's Seattle-Hawaii flights.
- Mention that live schedules and fares should be verified directly with Delta.

IMPORTANT RESEARCH LINK REQUIREMENTS:
For every major activity, restaurant, beach, hike, hotel area, or romantic idea, include actionable links:
- Google Maps search link
- Tripadvisor search link
- Yelp link for restaurants when relevant
- Official website search suggestion when useful

Do not invent review scores.
Instead, say what to look for in reviews:
- recent reviews
- parking comments
- crowding
- food quality
- reservation difficulty
- safety
- value
- whether it fits couples

PLEASE PROVIDE:

1. Three trip options:
   - Short trip
   - Medium trip
   - Longer trip

2. Recommended option and why.

3. Best island combination.

4. Detailed day-by-day itinerary.

5. Actionable activities with research links.

6. Romantic experiences with research links.

7. Great restaurants with review links.

8. Hidden gems with research links.

9. Budget estimate.

10. Packing list.

11. Suggested Delta flight strategy.

12. Whether we should spend more days before or after the wedding.

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
